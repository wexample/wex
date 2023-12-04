from addons.app.command.db.dump import app__db__dump
from addons.app.command.db.restore import app__db__restore
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from src.helper.file import file_remove_extension


class TestAppCommandDbRestore(AbstractAppTestCase):
    def test_restore(self) -> None:
        def callback(db_service: str) -> None:
            self.log(f"Testing database dump : {db_service}")

            app_dir = self.create_and_start_test_app(services=[db_service])

            response = self.kernel.run_function(
                app__db__dump,
                {
                    "app-dir": app_dir,
                },
            )

            dump_file = response.print_wrapped_str()

            self.assertPathExists(dump_file)

            self.kernel.run_function(
                app__db__restore, {"app-dir": app_dir, "file-path": dump_file}
            )

            # Test raw dump
            response = self.kernel.run_function(
                app__db__dump,
                {"app-dir": app_dir, "zip": False},
            )

            dump_file = response.print_wrapped_str()
            # Remove the file extension to make it match the format returned by unpacked files
            self.kernel.run_function(
                app__db__restore,
                {"app-dir": app_dir, "file-path": file_remove_extension(dump_file)},
            )

        self.for_each_db_service(callback)

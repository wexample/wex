from addons.app.command.db.dump import app__db__dump
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandDbDump(AbstractAppTestCase):
    def test_dump(self) -> None:
        def callback(db_service: str) -> None:
            self.log(f"Testing database dump : {db_service}")

            app_dir = self.create_and_start_test_app(
                services=[db_service], force_restart=True
            )

            response = self.kernel.run_function(
                app__db__dump,
                {
                    "app-dir": app_dir,
                },
            )

            path = response.print()
            assert isinstance(path, str)
            self.assertPathExists(path)

            self.stop_test_app(app_dir)

        self.for_each_db_service(callback)

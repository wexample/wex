from addons.app.command.db.dump import app__db__dump
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandDbDump(AbstractAppTestCase):
    def test_dump(self) -> None:
        def callback(db_service):
            self.log(f"Testing database restore : {db_service}")

            app_dir = self.create_and_start_test_app(services=[db_service])

            response = self.kernel.run_function(
                app__db__dump,
                {
                    "app-dir": app_dir,
                },
            )

            self.assertPathExists(response.print())

        self.for_each_db_service(callback)

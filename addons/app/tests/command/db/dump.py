from addons.app.command.db.dump import app__db__dump
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandDbDump(AbstractAppTestCase):
    def test_dump(self):
        app_dir = self.create_and_start_test_app(services=[
            'mysql_8'
        ])

        response = self.kernel.run_function(
            app__db__dump,
            {
                'app-dir': app_dir,
            }
        )

        self.assertPathExists(
            response.print()
        )

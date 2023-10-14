from addons.app.command.db.dump import app__db__dump
from addons.app.command.db.restore import app__db__restore
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandDbRestore(AbstractAppTestCase):
    def test_restore(self):
        app_dir = self.create_and_start_test_app(services=[
            'mysql_8'
        ])

        response = self.kernel.run_function(
            app__db__dump,
            {
                'app-dir': app_dir,
            }
        )

        dump_file = response.print()

        self.assertPathExists(
            dump_file
        )

        response = self.kernel.run_function(
            app__db__restore,
            {
                'app-dir': app_dir,
                'file-path': dump_file
            }
        )
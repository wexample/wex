from addons.app.command.app.restart import app__app__restart
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandAppRestart(AbstractAppTestCase):
    def test_restart(self):
        app_dir = self.create_and_start_test_app(services=['php'])

        self.kernel.run_function(
            app__app__restart, {
                'app-dir': app_dir
            }
        )

        self.kernel.run_function(
            app__app__restart, {
                'app-dir': app_dir
            }
        )

        self.stop_test_app()

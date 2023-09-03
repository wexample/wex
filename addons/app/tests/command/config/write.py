from addons.app.command.config.write import app__config__write
from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop
from tests.AbstractTestCase import AbstractTestCase
from addons.app.helpers.test import create_test_app


class TestAppCommandConfigWrite(AbstractTestCase):
    def test_write(self):
        app_dir = create_test_app(self.kernel)

        self.kernel.run_function(
            app__config__write, {
                'app-dir': app_dir
            }
        )

        self.kernel.run_function(
            app__app__start, {
                'app-dir': app_dir
            }
        )

        self.kernel.run_function(
            app__config__write, {
                'app-dir': app_dir
            }
        )

        self.kernel.run_function(
            app__app__stop, {
                'app-dir': app_dir
            }
        )

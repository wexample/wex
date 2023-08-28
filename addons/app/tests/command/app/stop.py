from addons.app.command.app.stop import app__app__stop
from tests.AbstractTestCase import AbstractTestCase
from addons.app.helpers.test import create_test_app
from addons.app.command.app.start import app__app__start


class TestAppCommandAppStopPy(AbstractTestCase):
    def test_stop(self):
        app_dir = create_test_app(self.kernel, services=['php-8'])

        self.kernel.exec_function(
            app__app__start, {
                'app-dir': app_dir
            }
        )

        self.kernel.exec_function(
            app__app__stop, {
                'app-dir': app_dir
            }
        )

from addons.app.command.app.serve import app__app__serve
from tests.AbstractTestCase import AbstractTestCase
from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop
from addons.app.helpers.test import create_test_app


class TestAppCommandAppServe(AbstractTestCase):
    def test_serve(self):
        app_dir = create_test_app(self.kernel, services=['php_8'])

        self.kernel.run_function(
            app__app__serve, {
                'app-dir': app_dir
            }
        )

        self.kernel.run_function(
            app__app__start, {
                'app-dir': app_dir
            }
        )

        self.kernel.run_function(
            app__app__serve, {
                'app-dir': app_dir
            }
        )

        self.kernel.run_function(
            app__app__stop, {
                'app-dir': app_dir
            }
        )

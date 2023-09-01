from addons.app.command.app.restart import app__app__restart
from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop
from tests.AbstractTestCase import AbstractTestCase
from addons.app.helpers.test import create_test_app


class TestAppCommandAppRestart(AbstractTestCase):
    def test_restart(self):
        app_dir = create_test_app(self.kernel, services=['php_8'])

        self.kernel.exec_function(
            app__app__restart, {
                'app-dir': app_dir
            }
        )

        # self.kernel.exec_function(
        #     app__app__start, {
        #         'app-dir': app_dir
        #     }
        # )
        #
        # self.kernel.exec_function(
        #     app__app__restart, {
        #         'app-dir': app_dir
        #     }
        # )
        #
        # self.kernel.exec_function(
        #     app__app__stop, {
        #         'app-dir': app_dir
        #     }
        # )

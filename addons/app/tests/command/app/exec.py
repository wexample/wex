from addons.app.command.app.exec import app__app__exec
from tests.AbstractTestCase import AbstractTestCase
from addons.app.helpers.test import create_test_app
from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop


class TestAppCommandAppExec(AbstractTestCase):
    def test_exec(self):
        app_dir = create_test_app(self.kernel, services=['php_8'])

        self.kernel.run_function(
            app__app__start, {
                'app-dir': app_dir
            }
        )

        response = self.kernel.run_function(
            app__app__exec, {
                'app-dir': app_dir,
                'command': 'echo TEST'
            }
        )

        self.assertEqual(
            response.first()[0],
            'TEST'
        )

        self.kernel.run_function(
            app__app__stop, {
                'app-dir': app_dir
            }
        )

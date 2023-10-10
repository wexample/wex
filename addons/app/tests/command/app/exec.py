from addons.app.command.app.exec import app__app__exec
from addons.app.command.app.stop import app__app__stop
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandAppExec(AbstractAppTestCase):
    def test_exec(self):
        app_dir = self.create_and_start_text_app(services=['php_8'])

        response = self.kernel.run_function(
            app__app__exec, {
                'app-dir': app_dir,
                'command': 'echo TEST'
            }
        )

        self.assertEqual(
            response.first(),
            'TEST'
        )

        self.kernel.run_function(
            app__app__stop, {
                'app-dir': app_dir
            }
        )
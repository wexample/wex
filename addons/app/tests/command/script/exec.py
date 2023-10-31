from addons.app.command.script.exec import app__script__exec
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandScriptExec(AbstractAppTestCase):
    def test_exec(self):
        app_dir = self.create_test_app(services=['php'])

        response = self.kernel.run_function(app__script__exec, {
            'name': 'missing',
            'app-dir': app_dir
        })

        self.assertIsNone(
            response.first()
        )

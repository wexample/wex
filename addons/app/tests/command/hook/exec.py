from addons.app.helpers.test import create_test_app
from tests.AbstractTestCase import AbstractTestCase
from addons.app.command.hook.exec import app__hook__exec
from src.const.globals import COMMAND_CHAR_APP


class TestAppCommandHookExec(AbstractTestCase):
    def test_exec(self):
        app_dir = create_test_app(self.kernel, services=['php_8'])

        results = self.kernel.run_function(
            app__hook__exec,
            {
                'app-dir': app_dir,
                'hook': 'missing/hook'
            }
        ).first()

        self.assertEqual(
            results['php_8'],
            None
        )

        self.assertEqual(
            results[COMMAND_CHAR_APP],
            None
        )

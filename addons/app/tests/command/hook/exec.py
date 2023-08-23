from addons.app.helpers.test import create_test_app
from tests.AbstractTestCase import AbstractTestCase
from addons.app.command.hook.exec import app__hook__exec


class TestAppCommandHookExec(AbstractTestCase):
    def test_exec(self):
        app_dir = create_test_app(self.kernel, services=['php-8'])

        service_results, app_result = self.kernel.exec_function(
            app__hook__exec,
            {
                'app-dir': app_dir,
                'hook': 'missing/hook'
            }
        )

        self.assertEqual(
            service_results['php-8'],
            None
        )

        self.assertEqual(
            app_result,
            None
        )

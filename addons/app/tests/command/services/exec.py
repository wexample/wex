from addons.app.helpers.test import create_test_app
from tests.AbstractTestCase import AbstractTestCase
from addons.app.command.services.exec import app__services__exec


class TestAppCommandServicesExec(AbstractTestCase):
    def test_exec(self):
        app_dir = create_test_app(self.kernel, services=['php-8'])

        response = self.kernel.exec_function(
            app__services__exec,
            {
                'app-dir': app_dir,
                'hook': 'hook/name'
            }
        )

        self.assertTrue(
            response['php-8'] is None
        )

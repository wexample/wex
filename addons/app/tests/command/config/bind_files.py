from addons.app.command.config.bind_files import app__config__bind_files
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandConfigBindFiles(AbstractAppTestCase):
    def test_bind_files(self):
        app_dir = self.create_and_start_text_app(services=['php_8'])

        response = self.kernel.run_function(
            app__config__bind_files,
            {
                'app-dir': app_dir,
                'dir': 'php'
            })

        self.assertTrue(
            'web_php_ini' in response.first()
        )

        self.assertTrue(
            isinstance(response.first()['web_php_ini'], str)
        )

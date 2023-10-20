from addons.app.command.services.exec import app__services__exec
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from src.const.error import ERR_COMMAND_FILE_NOT_FOUND


class TestAppCommandServicesExec(AbstractAppTestCase):
    def test_exec(self):
        app_dir = self.create_and_start_test_app(services=['php'])

        response = self.kernel.run_function(
            app__services__exec,
            {
                'app-dir': app_dir,
                'hook': 'hook/name'
            }
        )

        # The command does not exist
        self.assertEqual(
            response.first()['php'],
            None
        )

        self.stop_test_app()

from addons.app.command.db.exec import app__db__exec
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandDbExec(AbstractAppTestCase):
    def test_exec(self):
        def callback(db_service):
            self.log(f'Testing database exec {db_service}')

            exec_command = self.kernel.registry['services'][db_service]['config']['test']['exec_command']

            app_dir = self.create_and_start_test_app(services=[
                db_service
            ])

            response = self.kernel.run_function(
                app__db__exec,
                {
                    'app-dir': app_dir,
                    'command': exec_command
                }
            )

            self.assertTrue(
                response.print() != ''
            )

        self.for_each_db_service(callback)

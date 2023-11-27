from addons.app.command.db.exec import app__db__exec
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.command.resolver.ServiceCommandResolver import \
    ServiceCommandResolver


class TestAppCommandDbExec(AbstractAppTestCase):
    def test_exec(self):
        def callback(db_service):
            self.log(f'Testing database exec : {db_service}')
            service_resolver: 'ServiceCommandResolver' = self.kernel.resolvers[COMMAND_TYPE_SERVICE]
            registry_data = service_resolver.get_registry_data()
            test_config = registry_data[db_service]['config']['test']

            self.assertTrue(
                'exec_command' in test_config,
                'There is a test execution command if config file'
            )

            exec_command = test_config['exec_command']

            app_dir = self.create_and_start_test_app(services=[
                db_service
            ])

            response = self.kernel.run_function(
                app__db__exec,
                {
                    'app-dir': app_dir,
                    'command': exec_command,
                    'sync': True
                }
            )

            self.assertTrue(
                response.print() != ''
            )

        self.for_each_db_service(callback)

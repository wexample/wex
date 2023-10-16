from tests.AbstractTestCase import AbstractTestCase
from addons.app.helpers.test import create_test_app, create_test_app_dir
from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop


class AbstractAppTestCase(AbstractTestCase):
    def create_test_app(self, name: str | None = None, services: list | None = None) -> str:
        return create_test_app(
            self.kernel,
            name=name,
            services=services or [],
        )

    def start_test_app(self, name: str | None = None):
        response = self.kernel.run_function(
            app__app__start, {
                'app-dir': create_test_app_dir(self.kernel, name)
            }
        )

        shell_response = response.output_bag[6].print()

        self.log(shell_response)

        self.assertTrue(
            # Started does not guarantee that the container is fully working,
            # but it is sufficient in this case.
            shell_response.find('Started') > 0 or shell_response.find('Running') > 0,
        )

    def create_and_start_test_app(self, name: str | None = None, services: list | None = None) -> str:
        self.stop_test_app()

        app_dir = self.create_test_app(
            services=services,
        )

        self.start_test_app(name)

        return app_dir

    def stop_test_app(self, app_name: str | None = None):
        self.kernel.run_function(
            app__app__stop, {
                'app-dir': create_test_app_dir(self.kernel, app_name)
            }
        )

    def for_each_db_service(self, callback: callable):
        db_services = []

        services = self.kernel.registry['services']
        for service in services:
            if 'tags' in services[service]['config'] and 'db' in services[service]['config']['tags']:
                db_services.append(service)

        for db_service in db_services:
            callback(db_service)
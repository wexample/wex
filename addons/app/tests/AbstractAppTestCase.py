import os.path
import re

from src.helper.string import to_snake_case
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

        app_name_snake = to_snake_case(name or "test-app")

        patterns = [
            f"Container {app_name_snake}_test_.*  Creating",
            f"Container {app_name_snake}_test_.*  Started"
        ]

        shell_response = response.print()

        self.log(shell_response)

        self.assertTrue(
            # Started does not guarantee that the container is fully working,
            # but it is sufficient in this case.
            any(re.search(pattern, shell_response) for pattern in patterns),
        )

    def create_and_start_test_app(self, name: str | None = None, services: list | None = None) -> str:
        self.stop_test_app()

        app_dir = self.create_test_app(
            services=services,
        )

        self.start_test_app(name)

        return app_dir

    def stop_test_app(self, app_name: str | None = None):
        app_dir = create_test_app_dir(self.kernel, app_name)

        if not os.path.exists(app_dir):
            return

        self.kernel.run_function(
            app__app__stop, {
                'app-dir': app_dir
            }
        )

    def for_each_db_service(self, callback: callable):
        db_services = []

        services = self.kernel.registry['services']
        for service in services:
            if 'tags' in services[service]['config'] and 'db' in services[service]['config']['tags']:
                db_services.append(service)

        db_services = ['maria']

        for db_service in db_services:
            callback(db_service)

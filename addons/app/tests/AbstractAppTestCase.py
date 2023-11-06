import os.path
import re

from src.core.response.queue_collection.QueuedCollectionStopResponse import QueuedCollectionStopResponse
from src.helper.string import to_snake_case
from tests.AbstractTestCase import AbstractTestCase
from addons.app.helpers.test import create_test_app, build_test_app_name, DEFAULT_APP_TEST_NAME
from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop


class AbstractAppTestCase(AbstractTestCase):
    def create_test_app(
            self,
            name: str = DEFAULT_APP_TEST_NAME,
            services: list | None = None,
            force_restart: bool = False) -> str:
        return create_test_app(
            self.kernel,
            name=name,
            services=services or [],
            force_restart=force_restart
        )

    def start_test_app(
            self,
            app_dir: str,
            force_restart: bool = False):
        response = self.kernel.run_function(
            app__app__start, {
                'app-dir': app_dir
            }
        )

        first = response.first()
        if isinstance(first, QueuedCollectionStopResponse):
            if first.reason == 'APP_ALREADY_RUNNING' and not force_restart:
                return

        name = os.path.basename(app_dir.rstrip(os.sep))
        app_name_snake = to_snake_case(name)

        patterns = [
            f"Container {app_name_snake}_test_.*  Creating",
            f"Container {app_name_snake}_test_.*  Running",
            f"Container {app_name_snake}_test_.*  Started",
        ]

        shell_response = response.print()

        self.log(shell_response)

        self.assertTrue(
            # Started does not guarantee that the container is fully working,
            # but it is sufficient in this case.
            any(re.search(pattern, shell_response) for pattern in patterns),
        )

    def get_app_resources_path(self) -> str:
        return os.path.join(
            self.kernel.get_path('root'),
            'addons',
            'app',
            'tests',
            'resources',
        ) + os.sep

    def create_and_start_test_app(
            self,
            name: str = DEFAULT_APP_TEST_NAME,
            services: list | None = None,
            force_restart: bool = False) -> str:

        name = build_test_app_name(name, services)

        app_dir = self.create_test_app(
            name=name,
            services=services,
            force_restart=force_restart
        )

        if force_restart:
            self.stop_test_app(
                app_dir,
            )

        self.start_test_app(
            app_dir,
            force_restart=force_restart)

        return app_dir

    def stop_test_app(
            self,
            app_dir: str):
        if not os.path.exists(app_dir):
            return

        self.kernel.run_function(
            app__app__stop, {
                'app-dir': app_dir
            }
        )

    def for_each_db_service(self, callback: callable):
        db_services = []

        services = self.kernel.registry['service']
        for service in services:
            if 'tags' in services[service]['config'] and 'db' in services[service]['config']['tags']:
                db_services.append(service)

        for db_service in db_services:
            callback(db_service)

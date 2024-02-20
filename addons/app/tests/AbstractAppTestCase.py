import os.path
import re
import shutil
from typing import Optional, cast

from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.app.start import app__app__start
from addons.app.command.app.stop import app__app__stop
from addons.app.const.app import APP_FILEPATH_REL_ENV, APP_ENV_TEST
from addons.app.helper.test import (
    DEFAULT_APP_TEST_NAME,
    DEFAULT_ENVIRONMENT_TEST_REMOTE,
    DEFAULT_ENVIRONMENT_TEST_SERVER_PASSWORD,
    DEFAULT_ENVIRONMENT_TEST_SERVER_USERNAME,
    test_build_app_name,
    test_create_app,
)
from addons.default.command.file.append_once import default__file__append_once
from src.const.globals import COMMAND_TYPE_SERVICE
from src.const.types import AnyCallable, StringsList
from src.core.response.queue_collection.QueuedCollectionStopResponse import (
    QueuedCollectionStopResponse,
)
from src.helper.string import string_to_snake_case
from tests.AbstractTestCase import AbstractTestCase


class AbstractAppTestCase(AbstractTestCase):
    def create_test_app(
        self,
        name: str = DEFAULT_APP_TEST_NAME,
        services: Optional[StringsList] = None,
        force_restart: bool = False,
    ) -> str:
        return test_create_app(
            self.kernel, name=name, services=services or [], force_restart=force_restart
        )

    def reload_app_manager(self):
        # If current manager is in test app, config should be reloaded manually
        cast(AppAddonManager, self.kernel.addons["app"]).load_config()

    def start_test_app(self, app_dir: str, force_restart: bool = False) -> None:
        response = self.kernel.run_function(app__app__start, {
            "app-dir": app_dir,
            "env": APP_ENV_TEST,
        })

        first = response.first()
        if isinstance(first, QueuedCollectionStopResponse):
            if first.reason == "APP_ALREADY_RUNNING" and not force_restart:
                return

        name = os.path.basename(app_dir.rstrip(os.sep))
        app_name_snake = string_to_snake_case(name)

        patterns = [
            f"Container {app_name_snake}_test_.*  Creating",
            f"Container {app_name_snake}_test_.*  Created",
            f"Container {app_name_snake}_test_.*  Running",
            f"Container {app_name_snake}_test_.*  Started",
        ]

        shell_response = response.print_wrapped_str()

        self.log(shell_response)

        self.assertTrue(
            # Started does not guarantee that the container is fully working,
            # but it is sufficient in this case.
            any(re.search(pattern, shell_response) for pattern in patterns),
        )

    def get_app_resources_path(self) -> str:
        return self.kernel.get_path(
            "root",
            [
                "addons",
                "app",
                "tests",
                "resources",
            ],
        )

    def create_and_start_test_app(
        self,
        name: str = DEFAULT_APP_TEST_NAME,
        services: Optional[StringsList] = None,
        force_restart: bool = False,
    ) -> str:
        name = test_build_app_name(name, services)

        app_dir = self.create_test_app(
            name=name, services=services, force_restart=force_restart
        )

        if force_restart:
            self.stop_test_app(
                app_dir,
            )

        self.start_test_app(app_dir, force_restart=force_restart)

        return app_dir

    def stop_test_app(self, app_dir: str) -> bool:
        if not os.path.exists(app_dir):
            return False

        self.kernel.run_function(app__app__stop, {"app-dir": app_dir})

        return True

    def delete_test_app(self, app_dir: str) -> bool:
        exist = self.stop_test_app(app_dir)

        self.reset_workdir()

        if exist:
            shutil.rmtree(app_dir)

        return exist

    def for_each_db_service(self, callback: AnyCallable) -> None:
        db_services = []

        services = self.kernel.resolvers[COMMAND_TYPE_SERVICE].get_registry_data()
        for service in services:
            if (
                "tags" in services[service]["config"]
                and "db" in services[service]["config"]["tags"]
            ):
                db_services.append(service)

        for db_service in db_services:
            callback(db_service)

    def create_and_start_test_app_with_remote(
        self, services: StringsList
    ) -> AppAddonManager:
        environment = DEFAULT_ENVIRONMENT_TEST_REMOTE
        app_dir = self.create_and_start_test_app(services=services, force_restart=True)
        env_screaming_snake = string_to_snake_case(environment).upper()
        app_env_path = os.path.join(app_dir, APP_FILEPATH_REL_ENV)

        self.kernel.run_function(
            default__file__append_once,
            {
                "file": app_env_path,
                "line": f"ENV_{env_screaming_snake}_SERVER_USERNAME={DEFAULT_ENVIRONMENT_TEST_SERVER_USERNAME}",
            },
        )

        self.kernel.run_function(
            default__file__append_once,
            {
                "file": app_env_path,
                "line": f"ENV_{env_screaming_snake}_SERVER_PASSWORD={DEFAULT_ENVIRONMENT_TEST_SERVER_PASSWORD}",
            },
        )

        manager = AppAddonManager(self.kernel, app_dir=app_dir)
        manager.set_config("env.test_remote.server.ip", self.kernel.remote_address)

        return manager

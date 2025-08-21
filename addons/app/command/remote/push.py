import json
import os
from typing import TYPE_CHECKING, Optional

import requests
from wexample_helpers.helpers.string import string_to_snake_case

from addons.app.command.remote.exec import app__remote__exec
from addons.app.const.app import APP_ENV_PROD
from addons.app.decorator.app_command import app_command
from addons.app.helper.remote import (remote_build_temp_push_dir,
                                      remote_get_connexion_address,
                                      remote_get_connexion_options,
                                      remote_get_environment_ip,
                                      remote_get_login_command)
from src.const.globals import COMMAND_TYPE_ADDON, WEBHOOK_LISTEN_PORT_DEFAULT
from src.const.types import FileSystemStructureSchema
from src.core.response.DictResponse import DictResponse
from src.decorator.option import option
from src.helper.command import execute_command_sync

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON, should_be_valid=True)
@option(
    "--environment",
    "-e",
    type=str,
    required=True,
    help="Remote environment (dev, prod)",
)
def app__remote__push(
    manager: "AppAddonManager", environment: str, app_dir: str
) -> Optional[DictResponse]:
    domain_or_ip = remote_get_environment_ip(
        manager, environment, command=app__remote__push
    )

    connexion_address = remote_get_connexion_address(manager, environment)

    if not domain_or_ip or not connexion_address:
        return None

    if manager.get_env() == environment:
        manager.log(f"Unable to push to same environment {environment}")
        return None

    if environment == APP_ENV_PROD:
        manager.kernel.io.error(f"You don't want to do that on {environment}")
        return None

    def _app__remote__push_copy_to_remote(
        item_name: str, schema: FileSystemStructureSchema
    ) -> None:
        if (not "remote" in schema) or (schema["remote"] != "push"):
            return None

        item_realpath = os.path.realpath(item_name)
        remote_path = remote_build_temp_push_dir(environment, manager.get_app_name())

        # If item should be created, it will be checked on initialization.
        if os.path.exists(item_realpath):
            remote_item_path = os.path.join(remote_path, item_name)
            manager.log(
                f"Sending item {item_realpath} to {connexion_address}:{remote_item_path}"
            )

            if os.path.isfile(item_realpath):
                _create_remote_dir(os.path.dirname(remote_path))
                _send_file(item_realpath, remote_item_path)
            elif os.path.isdir(item_realpath):
                _send_directory(item_realpath, remote_item_path)

    def _create_remote_dir(remote_item_dir: str) -> None:
        manager.kernel.io.log(f"Creating remote dir {remote_item_dir}")
        manager.kernel.run_function(
            app__remote__exec,
            {
                "app-dir": manager.get_app_dir(),
                "environment": environment,
                "command": f"mkdir -p {remote_item_dir}",
            },
            # Do not enqueue execution
            fast_mode=True,
        )

    def _send_file(local_path: str, remote_path: str) -> None:
        # Ensure the remote directory is created before sending the file
        _create_remote_dir(os.path.dirname(remote_path))

        manager.kernel.io.log(f"Copying file to {remote_path}")
        execute_command_sync(
            manager.kernel,
            (
                remote_get_login_command(manager, environment)
                + ["scp"]
                + remote_get_connexion_options()
            )
            + [local_path, f"{connexion_address}:{remote_path}"],
        )

    def _send_directory(local_dir: str, remote_dir: str) -> None:
        for root, dirs, files in os.walk(local_dir):
            relative_path = os.path.relpath(root, local_dir)
            remote_root = os.path.join(remote_dir, relative_path)
            _create_remote_dir(remote_root)

            for file in files:
                local_file_path = os.path.join(root, file)
                remote_file_path = os.path.join(remote_root, file)
                _send_file(local_file_path, remote_file_path)

    manager.get_directory().process_schema_recursive(_app__remote__push_copy_to_remote)
    user = manager.get_env_var(
        f"ENV_{string_to_snake_case(environment).upper()}_SERVER_USERNAME"
    )
    webhook_port = manager.get_config(
        key="env.test_remote.webhook.port", default=WEBHOOK_LISTEN_PORT_DEFAULT
    ).get_int()

    url = f"http://{domain_or_ip}:{webhook_port}/webhook/addon/app/remote/push-receive?app={manager.get_app_name()}&env={environment}&user={user}"
    manager.log(f"GET {url}")
    response = requests.get(url)

    return DictResponse(
        kernel=manager.kernel,
        dictionary=json.loads(response.content.decode("utf-8")),
        title="Webhook response",
    )

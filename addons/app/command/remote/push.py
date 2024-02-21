import json
import os
from typing import TYPE_CHECKING, Union

import requests

from addons.app.command.remote.exec import app__remote__exec
from addons.app.decorator.app_command import app_command
from addons.app.helper.remote import (
    remote_get_connexion_address,
    remote_get_connexion_options,
    remote_get_environment_ip,
    remote_get_login_command,
)
from src.core.response.NullResponse import NullResponse
from src.core.response.DictResponse import DictResponse
from src.const.globals import COMMAND_TYPE_ADDON, WEBHOOK_LISTEN_PORT_DEFAULT
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
) -> Union[DictResponse, NullResponse]:
    domain_or_ip = remote_get_environment_ip(
        manager, environment, command=app__remote__push
    )

    connexion_address = remote_get_connexion_address(manager, environment)

    if not domain_or_ip or not connexion_address:
        return NullResponse

    def _app__remote__push_copy_to_remote(item_name, schema):
        if (not "remote" in schema) or (schema["remote"] != "push"):
            return

        item_realpath = os.path.realpath(item_name)
        remote_path = f"~/pushed/{environment}/{manager.get_config('global.name').get_str()}/"

        # If item should be created, it will be checked on regular path.
        if os.path.exists(item_realpath):
            remote_item_path = os.path.join(remote_path, item_name)
            manager.log(f"Sending file {item_realpath} to {connexion_address}:{remote_item_path}")

            if os.path.isfile(item_realpath):
                remote_item_dir = os.path.dirname(remote_item_path)
            else:
                remote_item_dir = remote_item_path

            manager.kernel.io.log(f"Creating remote dir {remote_item_dir}")
            manager.kernel.run_function(
                app__remote__exec,
                {
                    "app-dir": manager.get_app_dir(),
                    "environment": environment,
                    "command": f"mkdir -p {remote_item_dir}",
                },
            )

            if os.path.isfile(item_realpath):
                manager.kernel.io.log(f"Copying file {remote_item_dir}")
                execute_command_sync(
                    manager.kernel,
                    (
                        remote_get_login_command(manager, environment)
                        + [
                            "scp",
                        ]
                        + remote_get_connexion_options()
                    )
                    + [item_name, f"{connexion_address}:{remote_path}{item_name}"],
                )

    manager.get_directory().process_schema_recursive(_app__remote__push_copy_to_remote)

    url = f"http://{domain_or_ip}:{WEBHOOK_LISTEN_PORT_DEFAULT}/webhook/addon/app/remote/push-receive?app={manager.get_app_name()}&env={environment}"
    manager.log(f'GET {url}')
    response = requests.get(url)

    return DictResponse(
        kernel=manager.kernel,
        dictionary=json.loads(response.content.decode('utf-8')),
        title="Webhook response"
    )

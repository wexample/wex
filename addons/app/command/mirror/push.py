from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING
from src.helper.command import execute_command_sync
from dotenv import dotenv_values
import os
from src.helper.string import string_to_snake_case
from addons.app.const.app import APP_FILEPATH_REL_ENV
from addons.app.helper.remote import remote_get_environment_ip, remote_get_login_command
from addons.app.command.remote.exec import app__remote__exec

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option(
    "--environment",
    "-e",
    type=str,
    required=True,
    help="Remote environment (dev, prod)",
)
def app__mirror__push(manager: "AppAddonManager", environment: str, app_dir: str) -> bool:
    domain_or_ip = remote_get_environment_ip(manager, environment)

    if not domain_or_ip:
        return False

    env_screaming_snake = string_to_snake_case(environment).upper()
    app_env_path = os.path.join(app_dir, APP_FILEPATH_REL_ENV)

    username = dotenv_values(app_env_path).get(
        f"ENV_{env_screaming_snake}_SERVER_USERNAME")

    remote_path = f"/var/www/{environment}/{manager.get_config('global.name').get_str()}/"

    manager.kernel.run_function(
        app__remote__exec,
        {
            "app-dir": app_dir,
            "environment": environment,
            "command": f"mkdir -p {remote_path}"
        }
    )

    # TODO TMP, use sync directory schema instead.
    files = ["test.txt"]

    for file_path in files:
        command = remote_get_login_command(manager, environment) + [
            "scp",
            "-o",
            "StrictHostKeyChecking=no",
            file_path,
            f"{username}@{domain_or_ip}:{remote_path}test.txt"
        ]

        manager.log(f'Send file to {domain_or_ip} : {file_path}')
        execute_command_sync(
            manager.kernel,
            command)

    return True

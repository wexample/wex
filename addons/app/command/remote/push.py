import os
from typing import TYPE_CHECKING

from addons.app.command.remote.exec import app__remote__exec
from addons.app.decorator.app_command import app_command
from addons.app.helper.remote import (
    remote_get_connexion_address,
    remote_get_connexion_options,
    remote_get_environment_ip,
    remote_get_login_command,
)
from src.const.types import StringKeysDict
from src.const.globals import COMMAND_TYPE_ADDON
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
) -> bool:
    domain_or_ip = remote_get_environment_ip(
        manager, environment, command=app__remote__push
    )

    address = remote_get_connexion_address(manager, environment)

    if not domain_or_ip or not address:
        return False

    schema = manager.get_directory().get_schema()

    _push_schema_recursive(".", manager, environment, schema, address)

    return True


def _push_schema_recursive(
    item_name: str,
    manager: AppAddonManager,
    environment: str,
    schema: StringKeysDict,
    address: str,
) -> None:
    if "remote" in schema and schema["remote"] == "push":
        item_full_path = os.path.join(manager.get_app_dir(), item_name)
        remote_path = (
            f"~/pushed/{environment}/{manager.get_config('global.name').get_str()}/"
        )

        # If item should exist it will be checked on regular path.
        if os.path.exists(item_full_path):
            remote_item_path = os.path.join(remote_path, item_name)
            manager.log(
                f"Sending file {item_full_path} to {address}:{remote_item_path}"
            )

            if os.path.isfile(item_full_path):
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

            manager.kernel.io.log(f"Copying file {remote_item_dir}")
            if os.path.isfile(item_full_path):
                execute_command_sync(
                    manager.kernel,
                    (
                        remote_get_login_command(manager, environment)
                        + [
                            "scp",
                        ]
                        + remote_get_connexion_options()
                    )
                    + [item_name, f"{address}:{remote_path}{item_name}"],
                )

    if "schema" in schema:
        for child_item_name in schema["schema"]:
            _push_schema_recursive(
                os.path.join(item_name, child_item_name),
                manager,
                environment,
                schema["schema"][child_item_name],
                address,
            )

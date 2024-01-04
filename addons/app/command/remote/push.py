from src.core.file.AbstractFileSystemStructure import FileSystemStructureSchemaItem
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING
from src.helper.command import execute_command_sync
from addons.app.helper.remote import remote_get_environment_ip, remote_get_login_command, remote_get_connexion_address
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
def app__remote__push(manager: "AppAddonManager", environment: str, app_dir: str) -> bool:
    domain_or_ip = remote_get_environment_ip(manager, environment)

    if not domain_or_ip:
        return False

    remote_path = f"/var/www/{environment}/{manager.get_config('global.name').get_str()}/"

    manager.kernel.run_function(
        app__remote__exec,
        {
            "app-dir": app_dir,
            "environment": environment,
            "command": f"mkdir -p {remote_path}"
        }
    )

    address = remote_get_connexion_address(manager, environment)
    schema = manager.get_directory().get_schema()
    command_base = remote_get_login_command(manager, environment) + [
        "scp",
        "-o",
        "StrictHostKeyChecking=no",
    ]

    for item_name in schema:
        options: FileSystemStructureSchemaItem = schema[item_name]

        if "remote" in options and options["remote"] == "push":
            manager.log(f'Send file to {domain_or_ip} : {remote_path}{item_name}')
            execute_command_sync(
                manager.kernel,
                command_base + [
                    item_name,
                    f"{address}:{remote_path}{item_name}"
                ])

    return True

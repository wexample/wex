from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING
from addons.app.helper.remote import remote_get_environment_ip
from src.helper.command import execute_command_sync

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
    domain_or_ip = remote_get_environment_ip(manager.kernel, environment)

    if not domain_or_ip:
        return False

    remote_path = f"/var/www/{environment}/{manager.get_config('global.name').get_str()}/"
    # TODO Configure credentials
    command = ["sshpass", "-p", "TEST_PASSWORD", "ssh", "-o", "StrictHostKeyChecking=no", f"root@{domain_or_ip}",
               f"mkdir -p {remote_path}"]

    # Creating directory if missing
    execute_command_sync(
        manager.kernel,
        command)

    # TODO TMP, use sync directory schema instead.
    files = ["test.txt"]

    for file_path in files:
        command = [
            "sshpass",
            "-p",
            "TEST_PASSWORD",
            "scp",
            "-o",
            "StrictHostKeyChecking=no",
            file_path,
            f"root@{domain_or_ip}:{remote_path}test.txt"
        ]

        manager.log(f'Send file to {domain_or_ip} : {file_path}')
        execute_command_sync(
            manager.kernel,
            command)

    return True

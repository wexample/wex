from addons.app.decorator.app_command import app_command
from addons.app.helper.remote import remote_get_connexion_command, \
    remote_get_connexion_address
from src.helper.command import command_to_string
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.option import option
from typing import TYPE_CHECKING
from src.helper.args import args_parse_list_or_strings_list
from src.core.response.InteractiveShellCommandResponse import (
    InteractiveShellCommandResponse,
)

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option(
    "--command",
    "-c",
    type=str,
    required=True,
    help="Command to execute on remote server"
)
@option(
    "--environment",
    "-e",
    type=str,
    required=True,
    help="Remote environment (dev, prod)",
)
@option(
    "--terminal",
    "-t",
    type=bool,
    required=False,
    is_flag=True,
    help="Open a terminal",
)
def app__remote__exec(
    manager: "AppAddonManager",
    app_dir: str,
    environment: str,
    command: str,
    terminal: bool
) -> InteractiveShellCommandResponse:
    address = remote_get_connexion_address(manager=manager, environment=environment)

    if not address:
        return

    return InteractiveShellCommandResponse(
        manager.kernel,
        remote_get_connexion_command(manager=manager, environment=environment, terminal=terminal)
        + [
            address,
            f"'{command_to_string(args_parse_list_or_strings_list(command))}'"
        ]
    )

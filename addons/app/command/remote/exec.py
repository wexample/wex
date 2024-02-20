from typing import TYPE_CHECKING, Optional

from addons.app.decorator.app_command import app_command
from addons.app.helper.remote import (
    remote_get_connexion_address,
    remote_get_connexion_command,
)
from src.const.globals import COMMAND_TYPE_ADDON
from src.core.response.InteractiveShellCommandResponse import (
    InteractiveShellCommandResponse,
)
from src.decorator.option import option
from src.helper.args import args_parse_list_or_strings_list
from src.helper.command import command_to_string

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option(
    "--command",
    "-c",
    type=str,
    required=True,
    help="Command to execute on remote server",
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
    terminal: bool,
) -> Optional[InteractiveShellCommandResponse]:
    address = remote_get_connexion_address(
        manager=manager,
        environment=environment,
        command=app__remote__exec
    )

    if not address:
        return None

    return InteractiveShellCommandResponse(
        manager.kernel,
        remote_get_connexion_command(
            manager=manager, environment=environment, terminal=terminal
        )
        + [address, f"'{command_to_string(args_parse_list_or_strings_list(command))}'"],
    )

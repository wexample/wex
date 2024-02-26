from typing import TYPE_CHECKING, Optional, cast

from addons.app.command.remote.exec import app__remote__exec
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_ADDON, SHELL_DEFAULT
from src.core.response.InteractiveShellCommandResponse import (
    InteractiveShellCommandResponse,
)
from src.decorator.option import option

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
def app__remote__go(
    manager: "AppAddonManager", app_dir: str, environment: str
) -> Optional[InteractiveShellCommandResponse]:
    result = manager.kernel.run_function(
        app__remote__exec,
        {
            "app-dir": app_dir,
            "environment": environment,
            "terminal": True,
            "command": f'sh -c "cd /var/www/{environment}/{manager.get_app_name()}/ && {SHELL_DEFAULT}"',
        },
    ).first()

    if result:
        return cast(InteractiveShellCommandResponse, result)

    return None

from __future__ import annotations

from typing import TYPE_CHECKING, cast
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager
    from src.core.response.InteractiveShellCommandResponse import (
        InteractiveShellCommandResponse,
    )


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option(
    "--environment",
    "-e",
    type=str,
    required=True,
    help="Remote environment (dev, prod)",
)
def app__remote__go(
    manager: AppAddonManager, app_dir: str, environment: str
) -> InteractiveShellCommandResponse | None:
    from src.core.response.InteractiveShellCommandResponse import (
        InteractiveShellCommandResponse,
    )
    from addons.app.command.remote.exec import app__remote__exec
    from src.const.globals import SHELL_DEFAULT

    result = manager.kernel.run_function(
        app__remote__exec,
        {
            "app-dir": app_dir,
            "environment": environment,
            "terminal": True,
            "command": f'sh -c "cd /var/www/{environment}/{manager.get_app_name()} || cd /var/www/; {SHELL_DEFAULT}"',
        },
    ).first()

    if result:
        return cast(InteractiveShellCommandResponse, result)

    return None

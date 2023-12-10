from typing import TYPE_CHECKING, Optional

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_ADDON
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
    if manager.has_config(f"env.{environment}.server.ip"):
        ip = manager.get_config(f"env.{environment}.server.ip").get_str()
    elif manager.has_config(f"env.{environment}.domain_main"):
        ip = manager.get_config(f"env.{environment}.domain_main").get_str()
    else:
        return None

    app_name = manager.get_config("global.name").get_str()
    return InteractiveShellCommandResponse(
        manager.kernel,
        [
            "ssh",
            "-t",
            ip,
            f"\"sudo sh -c 'cd /var/www/{environment}/{app_name}/ && /bin/bash'\"",
        ],
    )

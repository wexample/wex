from typing import TYPE_CHECKING, Optional

from addons.app.decorator.app_command import app_command
from addons.app.helper.remote import remote_get_environment_ip
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
    domain_or_ip = remote_get_environment_ip(manager.kernel, environment)

    if not domain_or_ip:
        return

    app_name = manager.get_config("global.name").get_str()
    return InteractiveShellCommandResponse(
        manager.kernel,
        [
            "ssh",
            "-t",
            domain_or_ip,
            f"\"sudo sh -c 'cd /var/www/{environment}/{app_name}/ && /bin/bash'\"",
        ],
    )

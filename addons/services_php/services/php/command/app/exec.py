from typing import TYPE_CHECKING, Optional

from addons.app.decorator.app_command import app_command
from src.const.types import ShellCommandsList
from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(
    help="Return command to run when entering main container",
    command_type=COMMAND_TYPE_SERVICE,
    should_run=True,
)
@option("--container", "-c", type=str, required=False, help="Target container")
def php__app__exec(
    manager: "AppAddonManager", app_dir: str, service: str, container: None
) -> Optional[ShellCommandsList]:
    # Prevent returning data when entering another container.
    if container == service:
        return ["cd", "/var/www/html"]
    return None

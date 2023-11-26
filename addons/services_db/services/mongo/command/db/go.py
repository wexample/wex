from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Enter in db console", command_type=COMMAND_TYPE_SERVICE, should_run=True)
def mongo__db__go(manager: 'AppAddonManager', app_dir: str, service: str):
    return 'mongosh'

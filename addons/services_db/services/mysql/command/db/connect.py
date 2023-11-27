from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Return connexion info", command_type=COMMAND_TYPE_SERVICE)
def mysql__db__connect(manager: 'AppAddonManager', app_dir: str, service: str):
    return '--defaults-extra-file=/tmp/mysql.cnf'

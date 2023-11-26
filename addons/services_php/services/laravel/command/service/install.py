from src.helper.service import service_copy_sample_dir
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install service", command_type=COMMAND_TYPE_SERVICE)
def laravel__service__install(manager: 'AppAddonManager', app_dir: str, service: str):
    service_copy_sample_dir(manager.kernel, 'php', 'php')

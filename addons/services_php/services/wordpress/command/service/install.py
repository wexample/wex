from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Install service", command_type=COMMAND_TYPE_SERVICE)
def wordpress__service__install(kernel: 'Kernel', app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']

    manager.set_config(f'service.{service}', {
        'db_prefix': 'wp_'
    })

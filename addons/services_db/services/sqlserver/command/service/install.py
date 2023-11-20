from src.const.globals import PASSWORD_INSECURE
from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Install database service", command_type=COMMAND_TYPE_SERVICE)
def sqlserver__service__install(kernel: 'Kernel', app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']
    name = manager.get_config('global.name')
    manager.set_config(f'service.{service}', {
        'host': f'{name}_sqlserver',
        'name': name,
        'password': PASSWORD_INSECURE,
        'port': 1433,
        'user': 'sa',
    })

from src.decorator.option import option
from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Add special options to docker up command", command_type=COMMAND_TYPE_SERVICE)
@option('--options', '-o', required=True, default='', help="Argument")
def nextcloud__app__start_options(kernel: 'Kernel', app_dir: str, options: str, service: str):
    manager: AppAddonManager = kernel.addons['app']

    # On first start, do not run nextcloud until database is initialized.
    if not manager.get_config('global.initialized'):
        return [
            '--scale',
            f'{manager.get_config("global.name")}_nextcloud=0'
        ]

from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Install database service", command_type=COMMAND_TYPE_SERVICE)
def php__service__install(kernel: Kernel, app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']

    # Define itself as main container.
    manager.set_config(
        'global.main_service',
        manager.get_config(
            'global.main_service',
            service
        )
    )

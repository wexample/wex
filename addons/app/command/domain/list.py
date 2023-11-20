from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Description")
def app__domain__list(kernel: 'Kernel', app_dir: str):
    manager: AppAddonManager = kernel.addons['app']
    manager.build_runtime_config()

    return manager.get_runtime_config('domains')

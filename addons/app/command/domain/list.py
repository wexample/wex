from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_dir_option import app_dir_option
from src.core import Kernel
from src.decorator.command import command


@command(help="Description")
@app_dir_option()
def app__domain__list(kernel: Kernel, app_dir: str):
    manager: AppAddonManager = kernel.addons['app']
    manager.build_runtime_config()

    return manager.get_runtime_config('domains')


from src.const.globals import CORE_COMMAND_NAME
from src.decorator.command import command
from src.core import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager


@command(help="Return the configuration version number")
@app_dir_option()
def app__config__version(
        kernel: Kernel,
        app_dir: str):
    manager: AppAddonManager = kernel.addons['app']

    try:
        return manager.config[CORE_COMMAND_NAME]['version']
    except KeyError:
        # Used a older version.
        return '3.0.0'

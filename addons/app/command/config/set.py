from src.decorator.command import command
from src.decorator.option import option
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel


@command(help="Set a configuration setting for given app")
@option('--key', '-k', type=str, required=True,
              help="Key in config file")
@option('--value', '-v', required=True,
              help="Value to set")
@app_dir_option()
def app__config__set(
        kernel: Kernel,
        app_dir: str,
         key: str,
         value):

    manager: AppAddonManager = kernel.addons['app']

    return manager.set_config(key, value)

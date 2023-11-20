from src.decorator.option import option
from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Set a configuration setting for given app")
@option('--key', '-k', type=str, required=True,
        help="Key in config file")
@option('--value', '-v', required=True,
        help="Value to set")
def app__config__set(
        kernel: 'Kernel',
        app_dir: str,
        key: str,
        value):
    manager: AppAddonManager = kernel.addons['app']

    return manager.set_config(key, value)

from src.decorator.option import option
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from addons.app.decorator.app_command import app_command


@app_command(help="Get a configuration setting for given app")
@option('--key', '-k', type=str, required=True,
              help="Key in config file")
@option('--default', '-d', required=False,
              help="Default returned value if not found in config file")
def app__config__get(
        kernel: Kernel,
        app_dir: str,
        key: str,
        default: str = None
):
    manager: AppAddonManager = kernel.addons['app']

    return manager.get_config(key, default)

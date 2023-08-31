import click
from src.decorator.command import command
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel


@command()
@click.option('--key', '-k', type=str, required=True,
              help="Key in config file")
@click.option('--default', '-d', required=False,
              help="Default returned value if not found in config file")
@app_dir_option()
def app__config__get(
        kernel: Kernel,
        app_dir: str,
        key: str,
        default: str = None
):
    manager: AppAddonManager = kernel.addons['app']

    def callback():
        return manager.get_config(key, default)

    return manager.exec_in_workdir(
        app_dir,
        callback
    )


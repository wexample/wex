import click
from src.decorator.command import command
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel


@command()
@click.option('--key', '-k', type=str, required=True,
              help="Key in config file")
@click.option('--value', '-v', required=True,
              help="Value to set")
@click.option('--build', '-b', is_flag=True, required=False, default=False,
              help="Edit auto generated config or source config (default)")
@app_dir_option()
def app__config__set(
        kernel: Kernel,
        app_dir: str,
         key: str,
         value):

    manager: AppAddonManager = kernel.addons['app']

    return manager.set_config(key, value)

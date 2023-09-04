
from src.decorator.command import command
from src.decorator.option import option
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel


@command()
@app_dir_option()
@option('--options', '-o', required=True, default='', help="Argument")
def nextcloud__app__start_options(kernel: Kernel, app_dir, options: str):
    manager: AppAddonManager = kernel.addons['app']

    # On first start, do not run nextcloud until database is initialized.
    if not manager.get_config('global.initialized'):
        return [
            '--scale',
            f'{manager.get_config("global.name")}_nextcloud=0'
        ]

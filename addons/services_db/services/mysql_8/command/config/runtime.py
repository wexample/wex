from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.app.AppAddonManager import AppAddonManager


@command(help="Set configuration")
@app_dir_option()
@service_option()
def mysql_8__config__runtime(kernel: Kernel, app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']
    # Set db as main database.
    manager.set_runtime_config(
        f'db.main',
        manager.get_config(f'service.{service}'),
        False
    )



from src.const.globals import PASSWORD_INSECURE
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command()
@app_dir_option()
@service_option()
def mysql_8__service__install(kernel: Kernel, app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']
    name = manager.get_config('global.name')

    manager.set_config(service, {
        'host': f'{name}_mysql_8',
        'name': f'{name}',
        'password': PASSWORD_INSECURE,
        'port': 3306,
        'user': 'root',
    })

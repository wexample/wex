from src.const.globals import PASSWORD_INSECURE
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command(help="Install database service")
@app_dir_option()
@service_option()
def n8n__service__install(kernel: Kernel, app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']
    manager.set_config(f'service.{service}', {
        'basic_auth':{
            'user': 'admin',
            'password': PASSWORD_INSECURE,
        }
    })

import platform

from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command()
@app_dir_option()
@service_option()
def proxy__service__install(kernel: Kernel, app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']

    port = 80
    port_secure = 443

    # MacOS changes (not tested inherited code)
    if platform.system() == 'Darwin':
        port = 7780
        port_secure = 7743

    manager.set_config('global.port_public', port)
    manager.set_config('global.port_public_secure', port_secure)

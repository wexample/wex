import platform

from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command(help="Install the proxy service")
@app_dir_option()
@service_option()
def proxy__service__install(kernel: Kernel, app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']

    def callback():
        port = 80
        port_secure = 443

        # MacOS changes (not tested inherited code)
        if platform.system() == 'Darwin':
            port = 7780
            port_secure = 7743

        manager.set_config('global.port_public', port)
        manager.set_config('global.port_public_secure', port_secure)

    # TODO : Ensure this service hook is run from app work dir.
    #        We can create a decorator for that : @in_app_location
    #        Which is mandatory for all app commands
    manager.exec_in_workdir(
        app_dir,
        callback
    )

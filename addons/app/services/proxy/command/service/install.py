import os
import platform
import shutil

from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Install the proxy service", command_type=COMMAND_TYPE_SERVICE)
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

    shutil.copytree(
        os.path.join(kernel.registry['services']['proxy']['dir'], 'samples') + os.sep + 'proxy/',
        app_dir + 'proxy/',
        dirs_exist_ok=True,
        copy_function=shutil.copy2
    )

    # TODO : Ensure this service hook is run from app work dir.
    #        We can create a decorator for that : @in_app_location
    #        Which is mandatory for all app commands
    manager.exec_in_app_workdir(
        app_dir,
        callback
    )

    manager.set_config(
        'docker.main_container',
        manager.get_config(
            'docker.main_container',
            service
        )
    )

import os.path

from addons.app.const.app import APP_DIR_APP_DATA
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.option import option
from addons.app.command.app.exec import app__app__exec


@command(help="Set database permissions")
@app_dir_option()
@service_option()
@option('--file-name', '-f', type=str, required=True, help="Restore dump")
def mongo__db__restore(kernel: Kernel, app_dir: str, service: str, file_name: str):
    manager: AppAddonManager = kernel.addons['app']
    env_dir = f'{manager.app_dir}{APP_DIR_APP_DATA}'

    kernel.run_function(
        app__app__exec,
        {
            'app-dir': app_dir,
            'container-name': service,
            'command': [
                'mongorestore',
                '--drop',
                f'/dump/{file_name}',
            ],
            'sync': True
        }
    )

    return os.path.join(env_dir, service, 'dumps', file_name)

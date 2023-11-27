import os.path
from typing import TYPE_CHECKING

from addons.app.command.app.exec import app__app__exec
from addons.app.const.app import APP_DIR_APP_DATA
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Restore db dump", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option('--file-name', '-f', type=str, required=True, help="Restore dump")
def mongo__db__restore(manager: 'AppAddonManager', app_dir: str, service: str, file_name: str):
    env_dir = f'{manager.app_dir}{APP_DIR_APP_DATA}'

    manager.kernel.run_function(
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

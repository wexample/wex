import os.path

from addons.app.const.app import APP_DIR_APP_DATA
from src.core.Kernel import Kernel
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.option import option
from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Dump database", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option('--file-name', '-f', type=str, required=True, help="Dump file name")
def mongo__db__dump(kernel: Kernel, app_dir: str, service: str, file_name: str):
    manager: AppAddonManager = kernel.addons['app']
    env_dir = f'{manager.app_dir}{APP_DIR_APP_DATA}'

    kernel.run_function(
        app__app__exec,
        {
            'app-dir': app_dir,
            'container-name': service,
            'command': [
                'mongodump',
                '--out',
                f'/dump/{file_name}',
                '&&',
                # Change permissions to let
                # next script ton play with file
                'chmod',
                '777',
                f'-R',
                f'/dump/{file_name}',
                '>/dev/null',
                '2>&1'
            ],
            'sync': True
        }
    )

    return os.path.join(env_dir, service, 'dumps', file_name)

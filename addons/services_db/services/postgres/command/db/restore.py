from addons.services_db.services.postgres.command.db.connect import postgres__db__connect
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.option import option
from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Restore db dump", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option('--file-name', '-f', type=str, required=True, help="Dump file name")
def postgres__db__restore(kernel: 'Kernel', app_dir: str, service: str, file_name:str):
    manager: AppAddonManager = kernel.addons['app']

    command = [
        'postgres',
        kernel.run_function(
            postgres__db__connect,
            {
                'app-dir': app_dir,
                'service': service,
            },
            type=COMMAND_TYPE_SERVICE
        ).first(),
        manager.get_config('global.name'),
        '<',
        '/var/www/dumps/' + file_name
    ]

    kernel.run_function(
        app__app__exec,
        {
            'app-dir': app_dir,
            'container-name': service,
            # Ask to execute bash
            'command': command,
            'sync': True
        }
    )
import os.path

from addons.app.helper.db import get_db_service_dumps_path
from src.decorator.option import option
from addons.app.command.app.exec import app__app__exec
from addons.services_db.services.sqlserver.command.db.exec import sqlserver__db__exec
from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Dump database", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option('--file-name', '-f', type=str, required=True, help="Dump file name")
def sqlserver__db__dump(kernel: 'Kernel', app_dir: str, service: str, file_name: str):
    file_name += '.bak'
    manager: AppAddonManager = kernel.addons['app']
    app_name = manager.get_config('global.name')

    exec_command = kernel.run_function(
        sqlserver__db__exec,
        {
            'app-dir': app_dir,
            'service': service,
            'command': f"BACKUP DATABASE [{app_name}] TO DISK = '/var/opt/mssql/dumps/{file_name}'"
        },
        type=COMMAND_TYPE_SERVICE
    ).first()

    kernel.run_function(
        app__app__exec,
        {
            'app-dir': app_dir,
            'container-name': service,
            # Ask to execute bash
            'command': exec_command,
            'sync': True
        }
    )

    kernel.run_function(
        app__app__exec,
        {
            'app-dir': app_dir,
            'container-name': service,
            'user': 'root',
            # Ask to execute bash
            'command': [
                'chown',
                '1000:1000',
                f'/var/opt/mssql/dumps/{file_name}'
            ],
            'sync': True
        }
    )

    return os.path.join(
        get_db_service_dumps_path(kernel, service),
        file_name)

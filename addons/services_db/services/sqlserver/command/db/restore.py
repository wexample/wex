from addons.app.AppAddonManager import AppAddonManager
from src.decorator.option import option
from addons.app.command.app.exec import app__app__exec
from addons.services_db.services.sqlserver.command.db.exec import sqlserver__db__exec
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Restore db dump", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option('--file-name', '-f', type=str, required=True, help="Dump file name")
def sqlserver__db__restore(kernel: 'Kernel', app_dir: str, service: str, file_name: str):
    manager: AppAddonManager = kernel.addons['app']
    app_name = manager.get_config('global.name')

    exec_command = kernel.run_function(
        sqlserver__db__exec,
        {
            'app-dir': app_dir,
            'service': service,
            'command': f"USE master; ALTER DATABASE [{app_name}] "
                       f"SET SINGLE_USER WITH ROLLBACK IMMEDIATE; "
                       f"RESTORE DATABASE [{app_name}] FROM DISK = '/var/opt/mssql/dumps/{file_name}' "
                       f"WITH REPLACE; ALTER DATABASE [{app_name}] SET MULTI_USER;",
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

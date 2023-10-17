from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.option import option
from addons.app.command.app.exec import app__app__exec
from addons.services_db.services.sqlserver.command.db.exec import sqlserver__db__exec


@command(help="Set database permissions")
@app_dir_option()
@service_option()
@option('--file-name', '-f', type=str, required=True, help="Dump file name")
def sqlserver__db__restore(kernel: Kernel, app_dir: str, service: str, file_name: str):
    manager: AppAddonManager = kernel.addons['app']
    app_name = manager.get_config('global.name')

    print(file_name)

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

from typing import TYPE_CHECKING

from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from addons.services_db.services.sqlserver.command.db.exec import sqlserver__db__exec
from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Restore db dump", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option("--file-name", "-f", type=str, required=True, help="Dump file name")
@option("--database", "-d", type=str, required=False, help="Database name")
def sqlserver__db__restore(
    manager: "AppAddonManager", app_dir: str, service: str, file_name: str, database: str | None = None
) -> None:
    exec_command = manager.kernel.run_function(
        sqlserver__db__exec,
        {
            "app-dir": app_dir,
            "service": service,
            "command": f"USE master; ALTER DATABASE [{database}] "
            f"SET SINGLE_USER WITH ROLLBACK IMMEDIATE; "
            f"RESTORE DATABASE [{database}] FROM DISK = '/var/opt/mssql/dumps/{file_name}' "
            f"WITH REPLACE; ALTER DATABASE [{database}] SET MULTI_USER;",
        },
        type=COMMAND_TYPE_SERVICE,
    ).first()

    manager.kernel.run_function(
        app__app__exec,
        {
            "app-dir": app_dir,
            "container-name": service,
            # Ask to execute bash
            "command": exec_command,
            "sync": True,
        },
    )

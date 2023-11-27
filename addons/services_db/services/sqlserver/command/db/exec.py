from addons.services_db.services.sqlserver.command.db.go import sqlserver__db__go
from src.decorator.command import command
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Exec db query", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option('--command', '-c', type=str, required=True, help="Command to execute in database")
@option('--database', '-d', type=str, required=False, help="Database name")
def sqlserver__db__exec(manager: 'AppAddonManager', app_dir: str, service: str, command: str, database: Optional[str] = None):
    return manager.kernel.run_function(
        sqlserver__db__go,
        {
            'app-dir': app_dir,
            'service': service,
            'database': database,
        }, COMMAND_TYPE_SERVICE).first() + f' -h -1 -W -Q "SET NOCOUNT ON; {command}"'

from addons.services_db.services.sqlserver.command.db.go import sqlserver__db__go
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Exec db query", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option('--command', '-c', type=str, required=True, help="Command to execute in database")
@option('--database', '-d', type=str, required=False, help="Database name")
def sqlserver__db__exec(kernel: Kernel, app_dir: str, service: str, command: str, database: str = None):
    return kernel.run_function(
        sqlserver__db__go,
        {
            'app-dir': app_dir,
            'service': service,
            'database': database,
        }, COMMAND_TYPE_SERVICE).first() + f' -h -1 -W -Q "SET NOCOUNT ON; {command}"'

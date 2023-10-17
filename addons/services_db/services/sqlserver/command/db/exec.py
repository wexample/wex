from addons.services_db.services.sqlserver.command.db.go import sqlserver__db__go
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option


@command(help="Set database permissions")
@app_dir_option()
@service_option()
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

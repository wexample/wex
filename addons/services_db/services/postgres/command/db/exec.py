from addons.services_db.services.postgres.command.db.go import postgres__db__go
from src.decorator.command import command
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Exec db query", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option('--command', '-c', type=str, required=True, help="Command to execute in database")
@option('--database', '-d', type=str, required=False, help="Database name")
def postgres__db__exec(kernel: 'Kernel', app_dir: str, service: str, command: str, database: str = None):
    return kernel.run_function(
        postgres__db__go,
        {
            'app-dir': app_dir,
            'service': service,
            'database': database,
        }, COMMAND_TYPE_SERVICE).first() + f' --pset=pager=off -t -A -c "{command}"'

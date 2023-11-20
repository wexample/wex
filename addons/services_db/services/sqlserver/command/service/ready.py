from addons.services_db.services.sqlserver.command.db.exec import sqlserver__db__exec
from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Return true if database runs", command_type=COMMAND_TYPE_SERVICE, should_run=True)
def sqlserver__service__ready(kernel: 'Kernel', app_dir: str, service: str):
    exec_command = kernel.run_function(
        sqlserver__db__exec, {
            'app-dir': app_dir,
            'service': service,
            'command': 'SELECT 1',
            'database': 'master'
        }, COMMAND_TYPE_SERVICE
    ).print()

    response = kernel.run_function(
        app__app__exec,
        {
            'app-dir': app_dir,
            'container-name': service,
            # Ask to execute bash
            'command': exec_command,
            'sync': True
        }
    )

    first = response.first()
    if isinstance(first, list) and first[0] == '1':
        return True

    return False

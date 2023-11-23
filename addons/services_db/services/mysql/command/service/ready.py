from addons.app.command.app.exec import app__app__exec
from addons.services_db.services.mysql.command.db.connect import mysql__db__connect
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Return true if database runs", command_type=COMMAND_TYPE_SERVICE, should_run=True)
def mysql__service__ready(kernel: 'Kernel', app_dir: str, service: str):
    response = kernel.run_function(
        app__app__exec, {
            'app-dir': app_dir,
            'container-name': service,
            'command': [
                'mysqladmin',
                kernel.run_function(
                    mysql__db__connect,
                    {
                        'app-dir': app_dir,
                        'service': service,
                    },
                    type=COMMAND_TYPE_SERVICE
                ).first(),
                'ping'],
            'sync': True,
            'ignore-error': True
        }
    )

    if response.success and len(response.output_bag):
        return str(response.output_bag[0][0]).strip() == 'mysqld is alive'

    return response.success

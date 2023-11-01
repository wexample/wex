from src.core.Kernel import Kernel
from addons.app.command.app.exec import app__app__exec
from addons.services_db.services.mysql.command.db.connect import mysql__db__connect
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Return true if database runs", command_type=COMMAND_TYPE_SERVICE, should_run=True)
def mysql__service__ready(kernel: Kernel, app_dir: str, service: str):
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
            'sync': True
        }
    )

    return response.success

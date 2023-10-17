from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.app.command.app.exec import app__app__exec
from addons.services_db.services.mysql.command.db.connect import mysql__db__connect
from src.const.globals import COMMAND_TYPE_SERVICE


@command(help="Return true if database runs")
@app_dir_option()
@service_option()
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

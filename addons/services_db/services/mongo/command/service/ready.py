from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.services_db.services.mongo.command.db.exec import mongo__db__exec
from src.const.globals import COMMAND_TYPE_SERVICE
from addons.app.command.app.exec import app__app__exec


@command(help="Return true if database runs")
@app_dir_option()
@service_option()
def mongo__service__ready(kernel: Kernel, app_dir: str, service: str):
    exec_command = kernel.run_function(
        mongo__db__exec, {
            'app-dir': app_dir,
            'service': service,
            'command': 'db.runCommand({ ping: 1 })'
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

    return response.success

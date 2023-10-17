from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.services_db.services.postgres.command.db.exec import postgres__db__exec
from src.const.globals import COMMAND_TYPE_SERVICE


@command(help="Return true if database runs")
@app_dir_option()
@service_option()
def postgres__service__ready(kernel: Kernel, app_dir: str, service: str):
    response = kernel.run_function(
        postgres__db__exec, {
            'app-dir': app_dir,
            'service': service,
            'command': 'SELECT 1'
        }, COMMAND_TYPE_SERVICE
    )

    print(response.output_bag)

    return response.success

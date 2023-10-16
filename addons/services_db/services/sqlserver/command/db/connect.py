from addons.services_db.services.postgres.command.db.connect import postgres__db__connect
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from src.const.globals import COMMAND_TYPE_SERVICE


@command(help="Return connexion info")
@app_dir_option()
@service_option()
def sqlserver__db__connect(kernel: Kernel, app_dir: str, service: str):
    return kernel.run_function(postgres__db__connect, {
        'app-dir': app_dir,
        'service': service,
        'protocol': 'sqlserver'
    }, COMMAND_TYPE_SERVICE)

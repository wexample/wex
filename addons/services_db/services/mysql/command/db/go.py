from addons.services_db.services.mysql.command.db.connect import mysql__db__connect
from src.core.Kernel import Kernel
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Enter in db console", command_type=COMMAND_TYPE_SERVICE, should_run=True)
def mysql__db__go(kernel: Kernel, app_dir: str, service: str):
    return 'mysql ' + kernel.run_function(
        mysql__db__connect,
        {
            'app-dir': app_dir,
            'service': service,
        },
        type=COMMAND_TYPE_SERVICE
    ).first()

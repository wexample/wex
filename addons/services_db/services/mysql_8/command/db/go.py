from addons.services_db.services.mysql_8.command.db.connect import mysql_8__db__connect
from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command(help="Set database permissions")
@app_dir_option()
@service_option()
def mysql_8__db__go(kernel: Kernel, app_dir: str, service: str):
    return 'mysql ' + kernel.run_function(
        mysql_8__db__connect,
        {
            'app-dir': app_dir,
            'service': service,
        },
        type=COMMAND_TYPE_SERVICE
    ).first()
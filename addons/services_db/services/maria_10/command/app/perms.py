from addons.services_db.services.mysql_8.command.app.perms import mysql_8__app__perms
from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command(help="Set database permissions")
@app_dir_option()
@service_option()
def maria_10__app__perms(kernel: Kernel, app_dir: str, service: str):
    return kernel.run_function(
        mysql_8__app__perms,
        {
            'app-dir': app_dir,
            'service': service
        },
        type=COMMAND_TYPE_SERVICE
    )

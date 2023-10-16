from addons.services_db.services.mysql.command.db.go import mysql__db__go
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from src.const.globals import COMMAND_TYPE_SERVICE
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.option import option


@command(help="Set database permissions")
@app_dir_option()
@service_option()
@option('--command', '-c', type=str, required=True, help="Command to execute in database")
def mysql__db__exec(kernel: Kernel, app_dir: str, service: str, command: str):
    manager: AppAddonManager = kernel.addons['app']
    app_name = manager.get_config('global.name')

    return kernel.run_function(mysql__db__go, {
        'app-dir': app_dir,
        'service': service
    }, COMMAND_TYPE_SERVICE).first() + f' -s -N {app_name} -e "{command}"'

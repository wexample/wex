from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from src.decorator.option import option
from addons.services_db.services.mongo.command.db.go import mongo__db__go


@command(help="Set database permissions")
@app_dir_option()
@service_option()
@option('--command', '-c', type=str, required=True, help="Command to execute in database")
def mongo__db__exec(kernel: Kernel, app_dir: str, service: str, command: str):
    return kernel.run_function(mongo__db__go, {
        'app-dir': app_dir,
        'service': service
    }, COMMAND_TYPE_SERVICE).first() + f' --quiet --eval "{command}"'

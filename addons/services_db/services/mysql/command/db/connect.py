from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Return connexion info", command_type=COMMAND_TYPE_SERVICE)
def mysql__db__connect(kernel: 'Kernel', app_dir: str, service: str):
    return '--defaults-extra-file=/tmp/mysql.cnf'

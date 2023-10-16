from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command(help="Return connexion info")
@app_dir_option()
@service_option()
def mysql__db__connect(kernel: Kernel, app_dir: str, service: str):
    return '--defaults-extra-file=/tmp/mysql.cnf'

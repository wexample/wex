import os

from addons.app.AppAddonManager import AppAddonManager
from addons.app.const.app import APP_DIR_APP_DATA
from src.core.Kernel import Kernel
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Extra configuration", command_type=COMMAND_TYPE_SERVICE)
def mysql__config__write_post(kernel: Kernel, app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']
    manager.log(service + " : creating my.cnf file")

    # Create connexion file info
    my_conf_path = mysql_get_my_cnf_path(app_dir, service)

    # Create or overwrite the file
    with open(my_conf_path, "w") as file:
        file.write('[client]\n')
        file.write(f'user = "{manager.get_config("mysql.user")}"\n')
        file.write(f'password = "{manager.get_config("mysql.password")}"\n')


def mysql_get_my_cnf_path(app_dir: str, service: str) -> str:
    return os.path.join(
        app_dir,
        APP_DIR_APP_DATA,
        service,
        'my.cnf'
    )

import os

from addons.app.AppAddonManager import AppAddonManager
from addons.app.const.app import APP_DIR_APP_DATA
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command(help="Set database configuration")
@app_dir_option()
@service_option()
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

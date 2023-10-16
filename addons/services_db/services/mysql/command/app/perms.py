import os

from addons.app.AppAddonManager import AppAddonManager
from addons.services_db.services.mysql.command.config.write_post import mysql_get_my_cnf_path
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command(help="Set database permissions")
@app_dir_option()
@service_option()
def mysql__app__perms(kernel: Kernel, app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']
    manager.log(service + " : setting permissions to my.cnf")

    # Create connexion file info
    my_conf_path = mysql_get_my_cnf_path(app_dir, service)

    # Setting file permissions
    os.chmod(my_conf_path, 0o755)
    os.chmod(my_conf_path, 0o644)

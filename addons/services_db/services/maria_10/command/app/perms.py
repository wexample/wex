from addons.services_db.services.mysql_8.command.app.perms import mysql_8__app__perms
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command()
@app_dir_option()
@service_option()
def maria_10__app__perms(kernel: Kernel, app_dir: str, service: str):
    return mysql_8__app__perms(
        app_dir,
        service
    )

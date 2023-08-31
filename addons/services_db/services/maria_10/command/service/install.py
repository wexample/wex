from addons.services_db.services.mysql_8.command.service.install import mysql_8__service__install
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command()
@app_dir_option()
@service_option()
def maria_10__service__install(kernel: Kernel, app_dir: str, service: str):
    return mysql_8__service__install(
        app_dir,
        service
    )

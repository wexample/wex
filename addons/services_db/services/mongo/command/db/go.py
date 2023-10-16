from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command(help="Go to database")
@app_dir_option()
@service_option()
def mongo__db__go(kernel: Kernel, app_dir: str, service: str):
    return 'mongosh'

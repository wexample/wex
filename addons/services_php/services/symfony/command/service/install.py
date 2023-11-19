from src.helper.service import service_copy_sample_dir
from src.core.Kernel import Kernel
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Install service", command_type=COMMAND_TYPE_SERVICE)
def symfony__service__install(kernel: Kernel, app_dir: str, service: str):
    service_copy_sample_dir(kernel, 'php', 'php')

from src.helper.service import copy_service_sample_dir
from src.core.Kernel import Kernel
from addons.services_php.services.php.command.service.install import php__service__install
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Install service", command_type=COMMAND_TYPE_SERVICE)
def laravel__service__install(kernel: Kernel, app_dir: str, service: str):
    kernel.run_function(
        php__service__install,
        {
            'app-dir': app_dir,
            'service': service
        },
        COMMAND_TYPE_SERVICE
    )

    copy_service_sample_dir(kernel, 'php', 'php')
    # TODO Old version
    copy_service_sample_dir(kernel, 'php', 'apache')

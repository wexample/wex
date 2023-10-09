from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.Kernel import Kernel
from src.decorator.command import command
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from addons.services_php.services.php_8.command.service.install import php_8__service__install


@command(help="Install database service")
@app_dir_option()
@service_option()
def laravel_5__service__install(kernel: Kernel, app_dir: str, service: str):
    kernel.run_function(
        php_8__service__install,
        {
            'app-dir': app_dir,
            'service': service
        },
        COMMAND_TYPE_SERVICE
    )

from addons.services_php.services.php_8.command.config.write_compose_pre import php_8__config__write_compose_pre
from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command(help="Set configuration")
@app_dir_option()
@service_option()
def laravel_5__config__write_compose_pre(kernel: Kernel, app_dir: str, service: str):
    kernel.run_function(
        php_8__config__write_compose_pre,
        {
            'app-dir': app_dir,
            'service': service
        },
        COMMAND_TYPE_SERVICE
    )

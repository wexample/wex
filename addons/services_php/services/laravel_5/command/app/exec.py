from addons.services_php.services.php_8.command.app.exec import php_8__app__exec
from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option


@command(help="Return command to run when entering main container")
@app_dir_option()
@service_option()
@option('--container', '-c', type=str, required=False, help="Target container")
def laravel_5__app__exec(kernel: Kernel, app_dir: str, service: str, container: None):
    if container == service:
        return kernel.run_function(
            php_8__app__exec,
            {
                'app-dir': app_dir,
                'service': 'php_8',
                'container': 'php_8',
            },
            COMMAND_TYPE_SERVICE
        )

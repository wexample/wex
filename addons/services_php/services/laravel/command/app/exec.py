from addons.services_php.services.php.command.app.exec import php__app__exec
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Return command to run when entering main container", command_type=COMMAND_TYPE_SERVICE,
             should_run=True)
@option('--container', '-c', type=str, required=False, help="Target container")
def laravel__app__exec(kernel: 'Kernel', app_dir: str, service: str, container: None):
    if container == service:
        return kernel.run_function(
            php__app__exec,
            {
                'app-dir': app_dir,
                'service': 'php',
                'container': 'php',
            },
            COMMAND_TYPE_SERVICE
        )

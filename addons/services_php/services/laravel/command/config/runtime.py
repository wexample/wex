from addons.services_php.services.php.command.config.runtime import php__config__runtime
from src.core.Kernel import Kernel
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Set runtime configuration", command_type=COMMAND_TYPE_SERVICE)
def laravel__config__runtime(kernel: Kernel, app_dir: str, service: str):
    kernel.run_function(
        php__config__runtime,
        {
            'app-dir': app_dir,
            'service': service
        },
        COMMAND_TYPE_SERVICE
    )

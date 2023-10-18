from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.Kernel import Kernel
from src.decorator.command import command
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from addons.services_php.services.php.command.service.install import php__service__install
from addons.app.AppAddonManager import AppAddonManager


@command(help="Install service")
@app_dir_option()
@service_option()
def wordpress__service__install(kernel: Kernel, app_dir: str, service: str):
    kernel.run_function(
        php__service__install,
        {
            'app-dir': app_dir,
            'service': service
        },
        COMMAND_TYPE_SERVICE
    )

    manager: AppAddonManager = kernel.addons['app']
    manager.set_config(f'service.{service}', {
        'db_prefix': 'wp_'
    })

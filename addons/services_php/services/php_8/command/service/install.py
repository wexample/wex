from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command


@command(help="Install database service")
@app_dir_option()
@service_option()
def php_8__service__install(kernel: Kernel, app_dir: str, service: str):
    manager: AppAddonManager = kernel.addons['app']

    manager.set_config(
        'docker.main_container',
        manager.get_config(
            'docker.main_container',
            service
        )
    )

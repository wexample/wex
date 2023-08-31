from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from src.decorator.command import command
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option


@command()
@app_dir_option()
@service_option()
def app__service__used(kernel: Kernel, service: str, app_dir: str) -> bool:
    manager: AppAddonManager = kernel.addons['app']

    return service in manager.get_config('global.services')

from src.core.Kernel import Kernel
from addons.app.decorator.service_option import service_option
from addons.app.decorator.app_command import app_command


@app_command(help="Return ture if service is installed on app")
@service_option()
def app__service__used(kernel: Kernel, service: str, app_dir: str) -> bool:
    from addons.app.AppAddonManager import AppAddonManager
    manager: AppAddonManager = kernel.addons['app']

    return service in (manager.get_config('service') or {}).keys()

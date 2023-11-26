from addons.app.decorator.service_option import service_option
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Return ture if service is installed on app")
@service_option()
def app__service__used(manager: 'AppAddonManager', service: str, app_dir: str) -> bool:
    return service in (manager.get_config('service') or {}).keys()

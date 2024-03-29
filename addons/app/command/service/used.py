from typing import TYPE_CHECKING, cast

from addons.app.decorator.app_command import app_command
from addons.app.decorator.service_option import service_option
from src.const.types import RegistryAllServices

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Return true if service is installed on app")
@service_option()
def app__service__used(manager: "AppAddonManager", service: str, app_dir: str) -> bool:
    services = cast(RegistryAllServices, manager.get_config("service", {}).get_dict())
    return service in services.keys()

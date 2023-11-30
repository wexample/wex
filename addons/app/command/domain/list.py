from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.const.types import AppConfigValue

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Description")
def app__domain__list(manager: "AppAddonManager", app_dir: str) -> AppConfigValue:
    manager.build_runtime_config()

    return manager.get_runtime_config("domains")

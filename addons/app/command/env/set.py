from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from addons.app.helper.app import app_create_env
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Set APP_ENV value in .wex/.env file")
@option("--environment", "-e", type=str, required=True, help="Environment name")
def app__env__set(manager: "AppAddonManager", app_dir: str, environment: str) -> bool:
    return app_create_env(environment, manager.get_app_dir(), True)

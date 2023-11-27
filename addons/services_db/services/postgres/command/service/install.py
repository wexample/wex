from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE, PASSWORD_INSECURE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install database service", command_type=COMMAND_TYPE_SERVICE)
def postgres__service__install(manager: "AppAddonManager", app_dir: str, service: str):
    name = manager.get_config("global.name")
    manager.set_config(
        f"service.{service}",
        {
            "host": f"{name}_postgres",
            "name": f"{name}",
            "password": PASSWORD_INSECURE,
            "port": 5432,
            "user": "postgres",
        },
    )

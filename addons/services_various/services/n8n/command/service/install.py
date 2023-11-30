from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE, PASSWORD_INSECURE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install service", command_type=COMMAND_TYPE_SERVICE)
def n8n__service__install(manager: "AppAddonManager", app_dir: str, service: str) -> None:
    manager.set_config(
        f"service.{service}",
        {
            "basic_auth": {
                "user": "admin",
                "password": PASSWORD_INSECURE,
            }
        },
    )

from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.helper.string import string_random_password

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install database service", command_type=COMMAND_TYPE_SERVICE)
def mysql__service__install(
    manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    name = manager.get_config("global.name").get_str()
    manager.set_config(
        f"service.{service}",
        {
            "host": f"{name}_mysql",
            "name": f"{name}",
            "password": string_random_password(),
            "port": 3306,
            "user": "root",
        },
    )

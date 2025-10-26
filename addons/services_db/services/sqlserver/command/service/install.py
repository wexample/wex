from __future__ import annotations

from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install database service", command_type=COMMAND_TYPE_SERVICE)
def sqlserver__service__install(
    manager: AppAddonManager, app_dir: str, service: str
) -> None:
    from src.helper.string import string_random_password_secure

    name = manager.get_app_name()
    manager.set_config(
        f"service.{service}",
        {
            "host": f"{name}_sqlserver",
            "name": name,
            "password": string_random_password_secure(),
            "port": 1433,
            "user": "sa",
        },
    )

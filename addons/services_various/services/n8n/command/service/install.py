from __future__ import annotations

from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install service", command_type=COMMAND_TYPE_SERVICE)
def n8n__service__install(manager: AppAddonManager, app_dir: str, service: str) -> None:
    from src.helper.string import string_random_password

    manager.set_config(
        f"service.{service}",
        {
            "basic_auth": {
                "user": "admin",
                "password": string_random_password(),
            }
        },
    )

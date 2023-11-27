from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from addons.services_db.services.mysql.command.db.connect import mysql__db__connect
from src.const.globals import COMMAND_TYPE_SERVICE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(
    help="Enter in db console", command_type=COMMAND_TYPE_SERVICE, should_run=True
)
def mysql__db__go(manager: "AppAddonManager", app_dir: str, service: str):
    return (
        "mysql "
        + manager.kernel.run_function(
            mysql__db__connect,
            {
                "app-dir": app_dir,
                "service": service,
            },
            type=COMMAND_TYPE_SERVICE,
        ).first()
    )

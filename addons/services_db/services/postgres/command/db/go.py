from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from addons.services_db.services.postgres.command.db.connect import (
    postgres__db__connect,
)
from src.const.globals import COMMAND_TYPE_SERVICE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(
    help="Enter in db console", command_type=COMMAND_TYPE_SERVICE, should_run=True
)
def postgres__db__go(manager: "AppAddonManager", app_dir: str, service: str):
    return (
        "psql "
        + manager.kernel.run_function(
            postgres__db__connect,
            {
                "app-dir": app_dir,
                "service": service,
            },
            type=COMMAND_TYPE_SERVICE,
        ).first()
    )

from typing import TYPE_CHECKING

from addons.app.command.db.exec import app__db__exec
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Init database", command_type=COMMAND_TYPE_SERVICE, should_run=True)
def mongo__app__first_init(
    manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    manager.kernel.run_function(
        app__db__exec,
        {
            "app-dir": app_dir,
            # Ask to execute bash
            "command": "rs.initiate()",
            "sync": True,
        },
    )

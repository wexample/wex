from typing import TYPE_CHECKING

from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from addons.services_db.services.sqlserver.command.db.exec import sqlserver__db__exec
from src.const.globals import COMMAND_TYPE_SERVICE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(
    help="Return true if database runs",
    command_type=COMMAND_TYPE_SERVICE,
    should_run=True,
)
def sqlserver__service__ready(
    manager: "AppAddonManager", app_dir: str, service: str
) -> bool:
    manager.kernel.io.log("Waiting extra seconds for SQLServer...")
    import time
    time.sleep(30)

    exec_command = manager.kernel.run_function(
        sqlserver__db__exec,
        {
            "app-dir": app_dir,
            "service": service,
            "command": "SELECT 1",
            "database": "master",
        },
        COMMAND_TYPE_SERVICE,
    ).print()

    response = manager.kernel.run_function(
        app__app__exec,
        {
            "app-dir": app_dir,
            "container-name": service,
            # Ask to execute bash
            "command": exec_command,
            "sync": True,
            "ignore-error": True,
        },
    )

    first = response.first()
    if isinstance(first, list) and first[0] == "1":
        return True

    return False

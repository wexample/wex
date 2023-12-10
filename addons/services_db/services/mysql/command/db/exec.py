from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from addons.services_db.services.mysql.command.db.go import mysql__db__go
from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Exec db query", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option(
    "--command", "-c", type=str, required=True, help="Command to execute in database"
)
def mysql__db__exec(
    manager: "AppAddonManager", app_dir: str, service: str, command: str
) -> str:
    app_name = manager.get_config("global.name").get_str()

    return (
        manager.kernel.run_function(
            mysql__db__go,
            {"app-dir": app_dir, "service": service},
            COMMAND_TYPE_SERVICE,
        ).print_wrapped_str()
        + f' -s -N {app_name} -e "{command}"'
    )

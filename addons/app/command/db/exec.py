from typing import TYPE_CHECKING, Optional

from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Execute command in database container service")
@option(
    "--command", "-c", type=str, required=True, help="Command to execute in database"
)
@option("--database", "-d", type=str, required=False, help="Database name")
@option("--service", "-s", type=str, required=False, help="Database service name")
@option(
    "--sync",
    "-s",
    type=bool,
    is_flag=True,
    required=False,
    help="Execute command in a sub process",
)
def app__db__exec(
    manager: "AppAddonManager",
    app_dir: str,
    command: str,
    service: Optional[str] = None,
    database: Optional[str] = None,
    sync: bool = False,
):
    service = service or manager.get_config("docker.main_db_container", required=True)

    exec_command = manager.kernel.run_command(
        f"{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}db/exec",
        {
            "app-dir": app_dir,
            "service": service,
            "command": command,
            "database": database,
        },
    ).first()

    return manager.kernel.run_function(
        app__app__exec,
        {
            "app-dir": app_dir,
            "container-name": service,
            "command": exec_command,
            "sync": sync,
        },
    )

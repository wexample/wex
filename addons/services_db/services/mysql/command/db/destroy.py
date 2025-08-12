from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(
    help="Destroy database", command_type=COMMAND_TYPE_SERVICE, should_run=True
)
@option("--database", "-d", type=str, required=False, help="Database name")
@option(
    "--recreate",
    "-r",
    type=bool,
    required=False,
    default=True,
    help="Recreate an empty database",
)
def mysql__db__destroy(
    manager: "AppAddonManager",
    app_dir: str,
    service: str,
    database: str | None = None,
    recreate: bool = True,
) -> None:
    from addons.app.command.app.exec import app__app__exec
    from addons.services_db.services.mysql.command.db.connect import mysql__db__connect

    command = f"DROP DATABASE IF EXISTS {database}"

    if recreate:
        command += f"; CREATE DATABASE {database}"

    manager.log(f'Recreating an empty database "{database}"')
    manager.log(command)
    manager.kernel.run_function(
        app__app__exec,
        {
            "app-dir": app_dir,
            "container-name": service,
            # Ask to execute bash
            "command": [
                "mysql",
                manager.kernel.run_function(
                    mysql__db__connect,
                    {
                        "app-dir": app_dir,
                        "service": service,
                    },
                    type=COMMAND_TYPE_SERVICE,
                ).first(),
                "-e",
                f"'{command}'",
            ],
            "sync": True,
        },
    )

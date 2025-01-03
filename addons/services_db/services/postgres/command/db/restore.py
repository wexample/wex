from typing import TYPE_CHECKING

from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from addons.services_db.services.postgres.command.db.connect import (
    postgres__db__connect,
)
from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Restore db dump", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option("--file-name", "-f", type=str, required=True, help="Dump file name")
@option("--database", "-d", type=str, required=False, help="Database name")
def postgres__db__restore(
    manager: "AppAddonManager", app_dir: str, service: str, file_name: str, database: str | None = None
) -> None:
    command = [
        "psql",
        manager.kernel.run_function(
            postgres__db__connect,
            {
                "app-dir": app_dir,
                "service": service,
                "database": database,
            },
            type=COMMAND_TYPE_SERVICE,
        ).first(),
        database,
        "<",
        "/var/www/dumps/" + file_name,
    ]

    manager.kernel.run_function(
        app__app__exec,
        {
            "app-dir": app_dir,
            "container-name": service,
            # Ask to execute bash
            "command": command,
            "user": "postgres",
            "sync": True,
        },
    )

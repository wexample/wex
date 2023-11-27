import os.path
from typing import TYPE_CHECKING

from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from addons.app.helper.db import get_db_service_dumps_path
from addons.services_db.services.mysql.command.db.connect import mysql__db__connect
from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Dump database", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option("--file-name", "-f", type=str, required=True, help="Dump file name")
def mysql__db__dump(
    manager: "AppAddonManager", app_dir: str, service: str, file_name: str
):
    file_name += ".sql"

    command = [
        "mysqldump",
        manager.kernel.run_function(
            mysql__db__connect,
            {
                "app-dir": app_dir,
                "service": service,
            },
            type=COMMAND_TYPE_SERVICE,
        ).first(),
        manager.get_config("global.name"),
        ">",
        "/var/www/dumps/" + file_name,
    ]

    manager.kernel.run_function(
        app__app__exec,
        {
            "app-dir": app_dir,
            "container-name": service,
            # Ask to execute bash
            "command": command,
            "sync": True,
        },
    )

    return os.path.join(get_db_service_dumps_path(manager, service), file_name)

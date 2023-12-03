from typing import TYPE_CHECKING

from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from addons.services_db.services.mysql.command.db.connect import mysql__db__connect
from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.response.NonInteractiveShellCommandResponse import (
    NonInteractiveShellCommandResponse,
)

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(
    help="Return true if database runs",
    command_type=COMMAND_TYPE_SERVICE,
    should_run=True,
)
def mysql__service__ready(
    manager: "AppAddonManager", app_dir: str, service: str
) -> bool:
    response = manager.kernel.run_function(
        app__app__exec,
        {
            "app-dir": app_dir,
            "container-name": service,
            "command": [
                "mysqladmin",
                manager.kernel.run_function(
                    mysql__db__connect,
                    {
                        "app-dir": app_dir,
                        "service": service,
                    },
                    type=COMMAND_TYPE_SERVICE,
                ).first(),
                "ping",
            ],
            "sync": True,
            "ignore-error": True,
        },
    )

    assert isinstance(response, NonInteractiveShellCommandResponse)

    if response.success and len(response.output_bag):
        output_list = response.output_bag[0]
        assert isinstance(output_list, list)

        return str(output_list[0]).strip() == "mysqld is alive"

    return response.success is True

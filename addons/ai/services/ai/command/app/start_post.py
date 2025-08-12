from typing import TYPE_CHECKING, Optional

from addons.app.command.db.exec import app__db__exec
from addons.app.command.db.restore import app__db__restore
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.response.AbstractResponse import AbstractResponse

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Start the ai service", command_type=COMMAND_TYPE_SERVICE)
def ai__app__start_post(
    manager: "AppAddonManager", app_dir: str, service: str
) -> Optional[AbstractResponse]:
    response = manager.kernel.run_function(
        app__db__exec,
        {
            "app-dir": app_dir,
            # Ask to execute bash
            "command": "SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = 'assistant_conversation')",
            "sync": True,
        },
    )

    # In postgres, false == f and true == t
    if response.print_wrapped() == "f":
        return manager.kernel.run_function(
            app__db__restore,
            {
                "app-dir": app_dir,
                "file-path": manager.get_env_dir() + "postgres/dumps/init.sql",
            },
        )

    return None

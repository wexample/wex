from typing import TYPE_CHECKING

from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Start the proxy", command_type=COMMAND_TYPE_SERVICE, should_run=True)
def proxy__app__start_post(
    manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    commands = [
        ["ln", "-fs", "/proc/1/fd/1", "/var/log/nginx/access.log"],
        ["ln", "-fs", "/proc/1/fd/1", "/var/log/nginx/error.log"],
        ["nginx", "-s", "reload"],
    ]

    for command in commands:
        manager.kernel.run_function(
            app__app__exec,
            {
                "app-dir": app_dir,
                # Ask to execute bash
                "command": command,
                "sync": True,
            },
        )

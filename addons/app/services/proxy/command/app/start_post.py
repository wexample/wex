from typing import TYPE_CHECKING

from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from src.helper.command import execute_command_sync
from src.const.globals import COMMAND_TYPE_SERVICE
from src.helper.command import execute_command_sync

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Start the proxy", command_type=COMMAND_TYPE_SERVICE, should_run=True)
def proxy__app__start_post(
    manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    # TODO Pipeline inspect
    execute_command_sync(manager.kernel, ["docker", "ps"])
    execute_command_sync(manager.kernel, ["docker", "logs", "wex_proxy_local_proxy"])

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

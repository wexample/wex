from typing import TYPE_CHECKING

from addons.app.command.config.bind_files import app__config__bind_files
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Set runtime configuration", command_type=COMMAND_TYPE_SERVICE)
def php__config__runtime(
    manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    manager.kernel.run_function(
        app__config__bind_files, {"app-dir": app_dir, "dir": "php"}
    )

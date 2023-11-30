from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from addons.services_php.services.php.command.config.runtime import php__config__runtime
from src.const.globals import COMMAND_TYPE_SERVICE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Set runtime configuration", command_type=COMMAND_TYPE_SERVICE)
def laravel__config__runtime(manager: "AppAddonManager", app_dir: str, service: str) -> None:
    manager.kernel.run_function(
        php__config__runtime,
        {"app-dir": app_dir, "service": service},
        COMMAND_TYPE_SERVICE,
    )

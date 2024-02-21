from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from addons.services_php.services.php.command.service.install import php__service__install
from src.const.globals import COMMAND_TYPE_SERVICE
from src.helper.service import service_copy_sample_dir

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install service", command_type=COMMAND_TYPE_SERVICE)
def laravel__service__install(
    manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    manager.kernel.run_function(
        php__service__install,
        {
            "app-dir": app_dir,
            "service": "php",
        },
        type=COMMAND_TYPE_SERVICE
    )
    service_copy_sample_dir(manager.kernel, "php", "php")

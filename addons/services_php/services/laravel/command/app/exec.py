from typing import TYPE_CHECKING, Optional

from addons.app.decorator.app_command import app_command
from addons.services_php.services.php.command.app.exec import php__app__exec
from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.response.AbstractResponse import AbstractResponse
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(
    help="Return command to run when entering main container",
    command_type=COMMAND_TYPE_SERVICE,
    should_run=True,
)
@option("--container", "-c", type=str, required=False, help="Target container")
def laravel__app__exec(
    manager: "AppAddonManager", app_dir: str, service: str, container: None
) -> Optional[AbstractResponse]:
    if container == service:
        return manager.kernel.run_function(
            php__app__exec,
            {
                "app-dir": app_dir,
                "service": "php",
                "container": "php",
            },
            COMMAND_TYPE_SERVICE,
        )
    return None

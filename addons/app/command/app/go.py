from typing import TYPE_CHECKING

from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Enter into app container", should_run=True)
@option('--container-name', '-cn', type=str, required=False, help="Container name if not configured")
@option('--user', '-u', type=str, required=False, help="User name or uid")
def app__app__go(manager: 'AppAddonManager', app_dir: str, container_name: str | None = None, user: str | None = None):
    return manager.kernel.run_function(
        app__app__exec,
        {
            'app-dir': app_dir,
            'container-name': container_name or manager.get_main_container_name(),
            # Ask to execute bash
            'command': manager.get_service_shell(),
            'user': user,
            'interactive': True
        }
    )

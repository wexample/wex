from addons.app.command.app.exec import app__app__exec
from src.core import Kernel
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Enter into app container", should_run=True)
@option('--container-name', '-cn', type=str, required=False, help="Container name if not configured")
@option('--user', '-u', type=str, required=False, help="User name or uid")
def app__app__go(kernel: Kernel, app_dir: str, container_name: str | None = None, user: str | None = None):
    manager: AppAddonManager = kernel.addons['app']

    return kernel.run_function(
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

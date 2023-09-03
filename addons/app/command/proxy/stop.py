from addons.app.decorator.app_location_optional import app_location_optional
from addons.app.command.app.stop import app__app__stop
from src.decorator.as_sudo import as_sudo
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from src.decorator.command import command


@command()
@as_sudo
@app_location_optional
def app__proxy__stop(kernel: Kernel):
    manager: AppAddonManager = kernel.addons['app']
    manager.set_app_workdir(manager.proxy_path)

    # Execute command string to trigger middlewares
    kernel.run_function(
        app__app__stop,
        {
            'app-dir': manager.proxy_path
        }
    )

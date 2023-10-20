from addons.app.command.app.stop import app__app__stop
from src.decorator.as_sudo import as_sudo
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from src.decorator.command import command


@command(help="Stop the running reverse proxy server")
@as_sudo
def app__proxy__stop(kernel: Kernel):
    manager: AppAddonManager = kernel.addons['app']
    proxy_path = manager.get_proxy_path()
    manager.set_app_workdir(proxy_path)

    # Execute command string to trigger middlewares
    kernel.run_function(
        app__app__stop,
        {
            'app-dir': proxy_path
        }
    )

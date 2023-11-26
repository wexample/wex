from addons.app.command.app.stop import app__app__stop
from src.decorator.as_sudo import as_sudo
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.command import command
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@as_sudo()
@command(help="Stop the running reverse proxy server")
def app__proxy__stop(kernel: 'Kernel'):
    manager: AppAddonManager = cast(AppAddonManager, kernel.addons['app'])
    proxy_path = manager.get_proxy_path()
    manager.set_app_workdir(proxy_path)

    # Execute command string to trigger middlewares
    kernel.run_function(
        app__app__stop,
        {
            'app-dir': proxy_path
        }
    )

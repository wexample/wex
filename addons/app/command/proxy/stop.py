import os.path
from typing import TYPE_CHECKING, Optional, cast

from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.app.stop import app__app__stop
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@as_sudo()
@command(help="Stop the running reverse proxy server")
@option("--env", "-e", type=str, required=False, help="Env for accessing apps")
def app__proxy__stop(kernel: "Kernel", env: Optional[str] = None) -> None:
    manager: AppAddonManager = cast(AppAddonManager, kernel.addons["app"])
    proxy_path = manager.get_proxy_path(env)

    if os.path.exists(proxy_path):
        manager.set_app_workdir(proxy_path)

        # Execute command string to trigger middlewares
        kernel.run_function(app__app__stop, {"app-dir": proxy_path})

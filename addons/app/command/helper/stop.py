import os.path
from typing import TYPE_CHECKING, Optional, cast

from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.app.stop import app__app__stop
from addons.app.const.app import HELPER_APPS_LIST
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@as_sudo()
@command(help="Stop the running helper app")
@option(
    "--name",
    "-n",
    type=str,
    required=True,
    help=f"One of helper app name : {','.join(HELPER_APPS_LIST)}",
)
@option("--env", "-e", type=str, required=False, help="Env for accessing apps")
def app__helper__stop(kernel: "Kernel", name: str, env: Optional[str] = None) -> None:
    manager: AppAddonManager = cast(AppAddonManager, kernel.addons["app"])
    helper_app_path = manager.get_helper_app_path(name, env)

    if os.path.exists(helper_app_path):
        manager.set_app_workdir(helper_app_path)

        # Execute command string to trigger middlewares
        kernel.run_function(app__app__stop, {"app-dir": helper_app_path})

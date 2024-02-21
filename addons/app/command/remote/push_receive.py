from addons.app.helper.remote import remote_build_temp_push_dir
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command
from src.decorator.option import option
from typing import TYPE_CHECKING, cast
from addons.app.decorator.app_webhook import app_webhook
from addons.app.AppAddonManager import AppAddonManager

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_webhook()
@command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option('--app', '-a', type=str, required=True, help="Application name")
@option("--env", "-e", type=str, required=True, help="App environment")
def app__remote__push_receive(
    kernel: "Kernel",
    app: str,
    env: str
) -> None:
    manager = cast(AppAddonManager, kernel.addons["app"])
    print(manager.get_proxy_apps())

    return {
        "dir": remote_build_temp_push_dir(env, app),
        "app": app,
        "env": env,
    }

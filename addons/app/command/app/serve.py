from typing import TYPE_CHECKING

from addons.app.command.hook.exec import app__hook__exec
from addons.app.decorator.app_command import app_command

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Service the app if need a service to start.")
def app__app__serve(manager: "AppAddonManager", app_dir: str) -> None:
    manager.log("Serving app...")

    manager.kernel.run_function(
        app__hook__exec, {"app-dir": app_dir, "hook": "app/serve"}
    )

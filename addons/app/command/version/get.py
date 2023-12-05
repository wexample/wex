from addons.app.helper.app import app_create_manager
from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Description", dir_required=False)
def app__version__get(manager: "AppAddonManager", app_dir: str | None = None) -> str:
    manager = app_create_manager(manager.kernel, app_dir)

    return manager.get_config(
        f"global.version",
        None
    )

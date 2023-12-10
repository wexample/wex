import os
from typing import TYPE_CHECKING, Optional

from addons.app.decorator.app_command import app_command
from addons.app.helper.app import app_create_manager

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Description", dir_required=False)
def app__version__get(
    manager: "AppAddonManager", app_dir: str | None = None
) -> Optional[str]:
    manager = app_create_manager(manager.kernel, app_dir or os.getcwd())

    if manager.has_config(f"global.version"):
        return manager.get_config(f"global.version").get_str()

    return None

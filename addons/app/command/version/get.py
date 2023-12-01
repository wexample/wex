from typing import TYPE_CHECKING, Optional

from addons.app.decorator.app_command import app_command
from addons.default.helper.migration import migration_version_guess
from src.const.globals import CORE_COMMAND_NAME

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Description", dir_required=False)
def app__version__get(manager: "AppAddonManager", app_dir: str | None = None) -> str:
    app_version_string: Optional[str] = None
    try:
        # Trust regular config file
        app_version_string = str(manager.get_config(f"{CORE_COMMAND_NAME}.version"))
    except Exception:
        pass

    return app_version_string or str(
        migration_version_guess(manager.kernel, manager.get_app_dir_or_fail())
    )

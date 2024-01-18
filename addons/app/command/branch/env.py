from typing import TYPE_CHECKING, Optional

from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_ADDON
from src.const.types import StringKeysDict
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(
    help="Return env name for given branch as set in app config",
    command_type=COMMAND_TYPE_ADDON,
)
@option("--branch", "-b", type=str, required=True, help="Branch name")
def app__branch__env(
    manager: "AppAddonManager", branch: str, app_dir: str
) -> Optional[str]:
    return _app__branch__env(manager, branch)


def _app__branch__env(manager: "AppAddonManager", branch: str) -> Optional[str]:
    environments_config = manager.get_config(f"env").get_dict()

    for env in environments_config:
        env_config: StringKeysDict = environments_config[env]

        if "branch" in env_config and env_config["branch"] == branch:
            return env

    return None

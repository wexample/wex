from typing import TYPE_CHECKING, Optional

from addons.app.decorator.app_command import app_command
from addons.app.helper.remote import remote_get_environment_ip
from addons.app.helper.app import app_get_env_for_branch
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager

@app_command(
    help="Return server ip for given branch as set in app config",
    command_type=COMMAND_TYPE_ADDON,
)
@option("--branch", "-b", type=str, required=True, help="Branch name")
def app__branch__ip(
    manager: "AppAddonManager", branch: str, app_dir: str
) -> Optional[str]:
    env = app_get_env_for_branch(manager, branch)

    if env is not None:
        return remote_get_environment_ip(manager, env)

    return None

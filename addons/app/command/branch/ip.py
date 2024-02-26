from typing import TYPE_CHECKING, Optional

from addons.app.command.branch.env import _app__branch__env
from addons.app.decorator.app_command import app_command
from addons.app.helper.remote import remote_get_environment_ip
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
    env = _app__branch__env(manager, branch)

    if env is not None:
        return remote_get_environment_ip(manager, env, command=app__branch__ip)

    return None

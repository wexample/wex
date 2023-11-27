from typing import TYPE_CHECKING

from addons.app.command.env.get import app__env__get
from addons.app.command.hook.exec import app__hook__exec
from addons.app.const.app import APP_ENV_LOCAL
from addons.app.decorator.app_command import app_command
from src.const.globals import USER_WWW_DATA
from src.decorator.as_sudo import as_sudo
from src.helper.user import (
    get_user_or_sudo_user,
    set_owner_recursively,
    set_permissions_recursively,
    user_exists,
)

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@as_sudo()
@app_command(help="Set app files permissions")
def app__app__perms(manager: "AppAddonManager", app_dir: str):
    kernel = manager.kernel
    user = manager.get_config("permissions.user", None)

    if not user:
        env = kernel.run_function(
            app__env__get, {"app-dir": kernel.get_path("root")}
        ).first()

        # In local env get the "current" user, as it is probably
        # the code editor. In other envs, it uses www-data
        if env == APP_ENV_LOCAL:
            user = get_user_or_sudo_user()
        else:
            user = (
                USER_WWW_DATA if user_exists(USER_WWW_DATA) else get_user_or_sudo_user()
            )

    # If no group specified, set to None to guess it.
    group = manager.get_config("permissions.group", None)

    manager.log(f'Setting owner of all files to "{user}"')
    set_owner_recursively(app_dir, user, group)

    manager.log(f'Setting file mode of all files to "755"')
    set_permissions_recursively(app_dir, 0o755)

    manager.log("Updating app permissions...")
    kernel.run_function(app__hook__exec, {"app-dir": app_dir, "hook": "app/perms"})

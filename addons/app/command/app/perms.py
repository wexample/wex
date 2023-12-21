from typing import TYPE_CHECKING, Optional

from addons.app.command.env.get import _app__env__get
from addons.app.command.hook.exec import app__hook__exec
from addons.app.const.app import APP_ENV_LOCAL
from addons.app.decorator.app_command import app_command
from src.const.globals import USER_WWW_DATA
from src.decorator.as_sudo import as_sudo
from src.helper.user import (
    get_user_group_name,
    get_user_or_sudo_user,
    group_exists,
    set_owner_recursively,
    set_permissions_recursively,
    user_exists,
)

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@as_sudo()
@app_command(help="Set app files permissions")
def app__app__perms(manager: "AppAddonManager", app_dir: str) -> None:
    kernel = manager.kernel
    user: Optional[str | int]
    group: Optional[str | int]
    env = _app__env__get(kernel, kernel.directory.path)
    no_auto_local_config = manager.get_config_or_service_config(
        key="permissions.no_auto_local", service=None, default=False
    )
    auto_local = (
        not no_auto_local_config.is_bool() or not no_auto_local_config.get_bool()
    ) and env == APP_ENV_LOCAL

    # In local env get the "current" user, as it is probably
    # the code editor. In other envs, it uses www-data
    if auto_local:
        user = get_user_or_sudo_user()
    else:
        user_service_config = manager.get_config_or_service_config(
            key="permissions.user", service=None
        )

        if user_service_config.is_str():
            user = user_service_config.get_str()
        elif user_service_config.is_int():
            user = user_service_config.get_int()
        else:
            user = (
                USER_WWW_DATA if user_exists(USER_WWW_DATA) else get_user_or_sudo_user()
            )

    if isinstance(user, str) and not user_exists(user):
        kernel.io.error(
            f"User does not exists {user}, you can provide a uid instead", trace=False
        )

    if auto_local:
        group = get_user_group_name(get_user_or_sudo_user())
    else:
        # If no group specified, set to None to guess it.
        group_service_config = manager.get_config_or_service_config(
            "permissions.group", None
        )

        if group_service_config.is_str():
            group = group_service_config.get_str()
        elif group_service_config.is_int():
            group = group_service_config.get_int()
        elif isinstance(user, str):
            group = get_user_group_name(user)
        else:
            group = user

    if isinstance(group, str) and not group_exists(group):
        kernel.io.error(
            f"Group does not exists {group}, you can provide a gid instead", trace=False
        )

    manager.log(f'Setting owner of all files to "{user}:{str(group)}"')
    set_owner_recursively(app_dir, user, group)

    if manager.has_config("permissions.mode", int):
        mode = manager.get_config("permissions.mode").get_int()
    else:
        mode = manager.get_config_or_service_config(
            "permissions.mode", default=0o755
        ).get_int()

    manager.log(f'Setting file mode of all files to "{format(mode, "o")}"')
    set_permissions_recursively(app_dir, mode)

    manager.log("Updating app permissions...")
    kernel.run_function(app__hook__exec, {"app-dir": app_dir, "hook": "app/perms"})

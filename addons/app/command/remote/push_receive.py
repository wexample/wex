from addons.app.helper.remote import remote_build_temp_push_dir
from src.const.types import FileSystemStructureSchema
from src.helper.file import file_create_directories_and_copy
from src.helper.user import user_resolve_home_path
from src.const.globals import COMMAND_TYPE_ADDON, VERBOSITY_LEVEL_MAXIMUM
from src.decorator.command import command
from src.decorator.option import option
from typing import TYPE_CHECKING, cast, Optional
from addons.app.decorator.app_webhook import app_webhook
from addons.app.AppAddonManager import AppAddonManager

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_webhook()
@command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option('--app', '-a', type=str, required=True, help="Application name, used to find path")
@option("--env", "-e", type=str, required=True,
        help="App environment, a same application may exists in various environment")
@option("--user", "-u", type=str, required=True,
        help="User which initiated push, files should reside in its home directory")
def app__remote__push_receive(
    kernel: "Kernel",
    app: str,
    env: str,
    user: str,
) -> bool:
    app_dir = _app__remote__push_receive_find_app_dir(kernel, app, env)

    if not app_dir:
        return False

    manager = cast(AppAddonManager, kernel.addons["app"])
    manager.set_app_workdir(app_dir)
    user_temp_dir = remote_build_temp_push_dir(env, manager.get_app_name())

    def _app__remote__push_receive_copy_to_destination(item_name: str, schema: FileSystemStructureSchema) -> None:
        if ("remote" not in schema) or (schema["remote"] != "push"):
            return None

        temp_path_resolved = user_resolve_home_path(
            user_temp_dir + item_name, user
        )

        destination_path = app_dir + item_name

        manager.log(f"Copy {temp_path_resolved} to {destination_path}")

        file_create_directories_and_copy(
            temp_path_resolved,
            destination_path
        )

    def _app__remote__push_receive():
        manager.get_directory().process_schema_recursive(_app__remote__push_receive_copy_to_destination)

    manager.exec_in_app_workdir(
        app_dir,
        _app__remote__push_receive)

    return True


def _app__remote__push_receive_find_app_dir(kernel: "Kernel", app_name: str, env: str) -> Optional[str]:
    manager = cast(AppAddonManager, kernel.addons["app"])
    apps = manager.get_proxy_apps(env)

    if app_name not in apps:
        kernel.io.log('App not found in proxy apps', verbosity=VERBOSITY_LEVEL_MAXIMUM)
        return None

    return apps[app_name]

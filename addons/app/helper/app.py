import os
from typing import TYPE_CHECKING

from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.location.find import app__location__find
from addons.app.const.app import APP_DIR_APP_DATA, APP_FILE_APP_ENV
from src.helper.file import file_create_parent_and_touch

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def app_create_env(env: str, app_dir: str, rewrite: bool = True) -> bool:
    env_file_path = os.path.join(app_dir, APP_DIR_APP_DATA, APP_FILE_APP_ENV)

    # Check if the file already exists
    if os.path.exists(env_file_path) and not rewrite:
        return False

    file_create_parent_and_touch(env_file_path, f"APP_ENV={env}{os.linesep}")

    with open(env_file_path, "w") as f:
        f.write(f"APP_ENV={env}{os.linesep}")

    return True


def app_create_manager(kernel: "Kernel", app_dir: str) -> AppAddonManager:
    """
    Force manager create even dir is not a valid app.
    Useful to work with apps in an invalid state.
    """
    if not app_dir:
        app_dir = kernel.run_function(app__location__find).first()

        if not app_dir:
            app_dir = os.getcwd() + os.sep

    # Create a dedicated manager
    return AppAddonManager(kernel, app_dir=app_dir)

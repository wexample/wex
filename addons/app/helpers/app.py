import os

from addons.app.const.app import APP_DIR_APP_DATA, APP_FILE_APP_ENV
from src.helper.file import create_directories_and_file
from addons.app.command.location.find import app__location__find
from addons.app.AppAddonManager import AppAddonManager


def create_env(env, app_dir):
    create_directories_and_file(
        os.path.join(app_dir, APP_DIR_APP_DATA, APP_FILE_APP_ENV),
        f'APP_ENV={env}\n'
    )

    with open(os.path.join(app_dir, APP_DIR_APP_DATA, APP_FILE_APP_ENV), 'w') as f:
        f.write(f'APP_ENV={env}\n')


def create_manager(kernel, app_dir: str, name: str = 'app'):
    """
    Force manager create even dir is not a valid app.
    Useful to work with apps in an invalid state.
    """
    if not app_dir:
        app_dir = kernel.run_function(app__location__find).first()

        if not app_dir:
            app_dir = os.getcwd() + os.sep

    # Create a dedicated manager
    manager = AppAddonManager(kernel, name)
    manager.set_app_workdir(app_dir)

    return manager

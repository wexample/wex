import os

from addons.app.const.app import APP_DIR_APP_DATA, APP_FILE_APP_ENV
from src.helper.file import create_directories_and_file


def create_env(env, app_dir):
    create_directories_and_file(
        os.path.join(app_dir, APP_DIR_APP_DATA, APP_FILE_APP_ENV),
        f'APP_ENV={env}\n'
    )

    with open(os.path.join(app_dir, APP_DIR_APP_DATA, APP_FILE_APP_ENV), 'w') as f:
        f.write(f'APP_ENV={env}\n')


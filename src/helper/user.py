import os

from addons.app.const.app import APP_DIR_APP_DATA


def get_user_home_data_path():
    return f"{os.path.expanduser('~')}/{APP_DIR_APP_DATA}"

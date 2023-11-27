import os

from addons.app.AppAddonManager import AppAddonManager
from addons.app.const.app import APP_DIR_APP_DATA


def get_db_service_dumps_path(manager: 'AppAddonManager', service: str) -> str:
    return os.path.join(manager.app_dir, APP_DIR_APP_DATA, service, 'dumps')

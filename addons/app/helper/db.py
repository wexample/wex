import os
from addons.app.AppAddonManager import AppAddonManager
from addons.app.const.app import APP_DIR_APP_DATA


def get_db_service_dumps_path(kernel, service: str) -> str:
    manager: AppAddonManager = kernel.addons['app']
    env_dir = f'{manager.app_dir}{APP_DIR_APP_DATA}'
    return os.path.join(env_dir, service, 'dumps')

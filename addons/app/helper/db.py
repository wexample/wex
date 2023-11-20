import os
from addons.app.AppAddonManager import AppAddonManager
from addons.app.const.app import APP_DIR_APP_DATA
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def get_db_service_dumps_path(kernel: 'Kernel', service: str) -> str:
    manager: AppAddonManager = kernel.addons['app']
    return os.path.join(manager.app_dir, APP_DIR_APP_DATA, service, 'dumps')

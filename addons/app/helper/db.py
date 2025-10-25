from __future__ import annotations

import os

from addons.app.AppAddonManager import AppAddonManager


def get_db_service_dumps_path(manager: AppAddonManager, service: str) -> str:
    from addons.app.const.app import APP_DIR_APP_DATA
    return os.path.join(manager.get_app_dir(), APP_DIR_APP_DATA, service, "dumps")

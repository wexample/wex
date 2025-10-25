from __future__ import annotations
from typing import TYPE_CHECKING

from addons.app.AppAddonManager import AppAddonManager

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


def is_version_3_0_0(kernel: Kernel, path: str) -> bool | None:
    from addons.app.const.app import APP_DIR_APP_DATA_NAME
    if os.path.isfile(path + APP_DIR_APP_DATA_NAME):
        return True
    return None


def migration_3_0_0(kernel: Kernel, manager: AppAddonManager) -> None:
    # This is the older version.
    pass

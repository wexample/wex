import os.path
from typing import TYPE_CHECKING, Optional

from addons.app.AppAddonManager import AppAddonManager
from addons.app.const.app import APP_DIR_APP_DATA_NAME

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


def migration_3_0_0(kernel: "Kernel", manager: AppAddonManager) -> None:
    # This is the older version.
    pass


def is_version_3_0_0(kernel: "Kernel", path: str) -> Optional[bool]:
    if os.path.isfile(path + APP_DIR_APP_DATA_NAME):
        return True
    return None

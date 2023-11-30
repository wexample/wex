import os.path
from typing import TYPE_CHECKING, Optional

from addons.app.AppAddonManager import AppAddonManager

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def migration_3_0_0(kernel: "Kernel", manager: AppAddonManager) -> None:
    # This is the older version.
    pass


def is_version_3_0_0(kernel: "Kernel", path: str) -> Optional[bool]:
    if os.path.isfile(path + ".wex"):
        return True
    return None

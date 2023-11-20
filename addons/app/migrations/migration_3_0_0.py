import os.path

from addons.app.AppAddonManager import AppAddonManager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def migration_3_0_0(kernel: 'Kernel', manager: AppAddonManager):
    # This is the older version.
    pass


def is_version_3_0_0(kernel: 'Kernel', path: str):
    if os.path.isfile(path + '.wex'):
        return True
    return None

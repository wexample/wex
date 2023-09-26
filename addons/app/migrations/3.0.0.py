import os.path

from src.core import Kernel
from addons.app.AppAddonManager import AppAddonManager


def migration_3_0_0(kernel: Kernel, manager: AppAddonManager):
    # This is the older version.
    pass


def is_version_3_0_0(kernel: Kernel, path: str):
    if os.path.isfile(path + '.wex'):
        return True
    return None

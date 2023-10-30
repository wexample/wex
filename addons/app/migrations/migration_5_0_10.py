from src.helper.prompt import progress_steps
from src.core import Kernel
from addons.app.AppAddonManager import AppAddonManager


def migration_5_0_10(kernel: Kernel, manager: AppAddonManager):
    def _migration_5_0_10_update_config():
        manager.set_config('global.version', '1.0.0')

    progress_steps(kernel, [
        _migration_5_0_10_update_config,
    ])

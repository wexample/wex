from src.helper.prompt import progress_steps
from src.core import Kernel
from addons.app.AppAddonManager import AppAddonManager


def migration_5_0_34(kernel: Kernel, manager: AppAddonManager):
    def _migration_5_0_34_update_config():
        main_service = manager.get_config('docker.main_container', None)
        manager.set_config(
            'global.main_service',
            main_service)

        manager.remove_config('docker.main_container')

    progress_steps(kernel, [
        _migration_5_0_34_update_config,
    ])

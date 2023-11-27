from typing import TYPE_CHECKING

from addons.app.AppAddonManager import AppAddonManager
from src.helper.prompt import prompt_progress_steps

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def migration_5_0_10(kernel: "Kernel", manager: AppAddonManager):
    def _migration_5_0_10_update_config():
        manager.set_config("global.version", "1.0.0")

    prompt_progress_steps(
        kernel,
        [
            _migration_5_0_10_update_config,
        ],
    )

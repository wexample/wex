from typing import TYPE_CHECKING

from addons.app.AppAddonManager import AppAddonManager
from src.const.globals import VERSION_DEFAULT
from src.helper.prompt import prompt_progress_steps

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


def migration_5_0_10(kernel: "Kernel", manager: AppAddonManager) -> None:
    def _migration_5_0_10_update_config() -> None:
        manager.set_config("global.version", VERSION_DEFAULT)

    prompt_progress_steps(
        kernel,
        [
            _migration_5_0_10_update_config,
        ],
    )

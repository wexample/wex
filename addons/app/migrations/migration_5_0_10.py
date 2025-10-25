from __future__ import annotations

from typing import TYPE_CHECKING

from addons.app.AppAddonManager import AppAddonManager

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


def migration_5_0_10(kernel: Kernel, manager: AppAddonManager) -> None:
    from src.helper.prompt import prompt_progress_steps
    def _migration_5_0_10_update_config() -> None:
        from src.const.globals import VERSION_DEFAULT
        manager.set_config("global.version", VERSION_DEFAULT)

    prompt_progress_steps(
        kernel,
        [
            _migration_5_0_10_update_config,
        ],
    )

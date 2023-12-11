from typing import TYPE_CHECKING

from addons.app.AppAddonManager import AppAddonManager
from src.helper.prompt import prompt_progress_steps

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def migration_5_0_34(kernel: "Kernel", manager: AppAddonManager) -> None:
    def _migration_5_0_34_update_config() -> None:
        if manager.has_config("docker.main_container"):
            manager.set_config(
                "global.main_service",
                manager.get_config("docker.main_container").get_str(),
            )

        manager.remove_config("docker.main_container")

    prompt_progress_steps(
        kernel,
        [
            _migration_5_0_34_update_config,
        ],
    )

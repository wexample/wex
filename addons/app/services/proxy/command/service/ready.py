from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from addons.app.helper.docker import docker_build_long_container_name
from src.helper.command import execute_command_sync
from src.const.globals import COMMAND_TYPE_SERVICE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager

TEST_COUNT = 0


@app_command(
    help="Return true if database runs",
    command_type=COMMAND_TYPE_SERVICE,
    should_run=True,
)
def proxy__service__ready(
    manager: "AppAddonManager", app_dir: str, service: str
) -> bool:
    # for container_name in list:
    success, running_containers = execute_command_sync(
        manager.kernel, [
            "docker",
            "inspect",
            "--format",
            "'{{.State.Running}}'",
            docker_build_long_container_name(
                manager.kernel,
                manager.get_main_container_name())
        ]
    )

    return success

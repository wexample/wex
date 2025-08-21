from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from addons.app.helper.docker import docker_build_long_container_name
from src.core.response.InteractiveShellCommandResponse import \
    InteractiveShellCommandResponse
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Follow logs", should_run=True)
@option(
    "--tail",
    "-t",
    type=int,
    default=100,
    help="Tail length",
)
@option(
    "--container-name",
    "-cn",
    type=str,
    required=False,
    help="Container name if not configured",
)
def app__logs__follow(
    manager: "AppAddonManager",
    app_dir: str,
    tail: int,
    container_name: str | None = None,
) -> InteractiveShellCommandResponse:
    container_name = container_name or manager.get_main_container_name()

    return InteractiveShellCommandResponse(
        manager.kernel,
        [
            "docker",
            "logs",
            docker_build_long_container_name(manager.kernel, container_name),
            "--tail",
            str(tail),
            "-f",
        ],
    )

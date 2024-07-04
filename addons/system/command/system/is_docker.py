from typing import TYPE_CHECKING

from addons.app.helper.docker import docker_is_current
from src.decorator.command import command

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


@command(help="Return true if current environment is a Docker container")
def system__system__is_docker(kernel: "Kernel") -> bool:
    return docker_is_current()

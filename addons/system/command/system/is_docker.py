import os
from typing import TYPE_CHECKING

from src.decorator.command import command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Return true if current environment is a Docker container")
def system__system__is_docker(kernel: "Kernel") -> bool:
    return os.path.exists("/.dockerenv")

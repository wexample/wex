import os

from src.core.Kernel import Kernel
from src.decorator.command import command


@command(help="Return true if current environment is a Docker container")
def system__system__is_docker(kernel: Kernel):
    return os.path.exists('/.dockerenv')

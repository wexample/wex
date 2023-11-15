from src.helper.core import core_kernel_get_version
from src.decorator.command import command
from src.core import Kernel
from src.decorator.alias import alias


@alias('-v')
@alias('-version')
@alias('--v')
@alias('--version')
@alias('version')
@command(help="Returns core version")
def core__version__get(kernel: Kernel):
    return core_kernel_get_version(kernel)

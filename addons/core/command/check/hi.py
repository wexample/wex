from typing import TYPE_CHECKING

from src.decorator.alias import alias
from src.decorator.command import command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@alias('hi')
@command(help="Return hi! Used to check if core vitals are working")
def core__check__hi(kernel: 'Kernel'):
    return 'hi!'

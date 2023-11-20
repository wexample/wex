from src.decorator.command import command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Return a string")
def test__return_type__null(kernel: 'Kernel'):
    return

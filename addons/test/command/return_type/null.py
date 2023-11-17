from src.decorator.command import command
from src.core import Kernel


@command(help="Return a string")
def test__return_type__null(kernel: Kernel):
    return

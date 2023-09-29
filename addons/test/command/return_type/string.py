from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel


@command(help="Return a string")
@option('--arg', '-a', type=str, required=True, help="Argument")
def test__return_type__string(kernel: Kernel, arg):
    return str(arg)

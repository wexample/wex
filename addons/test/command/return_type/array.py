from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel


@command(help="Return an array")
@option('--arg', '-a', type=str, required=True, help="Argument")
def test__return_type__array(kernel: Kernel, arg):
    return [arg]
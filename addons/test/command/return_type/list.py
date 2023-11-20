from src.decorator.command import command
from src.decorator.option import option
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Return a list")
@option('--arg', '-a', type=str, required=True, help="Argument")
def test__return_type__list(kernel: 'Kernel', arg):
    return [arg]
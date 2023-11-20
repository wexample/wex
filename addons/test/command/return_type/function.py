from src.decorator.command import command
from src.decorator.option import option
from src.const.globals import COMMAND_TYPE_ADDON
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Return a function response", command_type=COMMAND_TYPE_ADDON)
@option('--arg', '-a', type=str, required=True, help="Argument")
def test__return_type__function(kernel: 'Kernel', arg):
    return _test__return_type__function


def _test__return_type__function():
    return 'FUNCTION_OK'

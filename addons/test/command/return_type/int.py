from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON


@command(help="Return an int value", command_type=COMMAND_TYPE_ADDON)
@option('--arg', '-a', type=int, required=True, help="Int value to add")
def test__return_type__int(kernel: Kernel, arg: int = 0):
    return 1 + arg
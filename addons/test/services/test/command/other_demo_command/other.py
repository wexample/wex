from src.decorator.test_command import test_command
from src.decorator.option import option
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

@test_command(command_type=COMMAND_TYPE_SERVICE)
@option('--option', '-o', is_flag=True, required=False,
        help="A first option as flag")
@option('--another-option', '-ao', is_flag=True, required=False,
        help="Another option")
def test__other_demo_command__other(kernel: 'Kernel', service:str, option=None, another_option=None):
    return 'FIRST'

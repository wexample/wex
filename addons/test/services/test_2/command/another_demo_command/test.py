from typing import TYPE_CHECKING

from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option
from src.decorator.test_command import test_command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@test_command(command_type=COMMAND_TYPE_SERVICE)
@option('--option', '-o', is_flag=True, required=False,
        help="A first option as flag")
@option('--another-option', '-ao', is_flag=True, required=False,
        help="Another option")
def test_2__another_demo_command__test(kernel: 'Kernel', service:str, option=None, another_option=None):
    return 'FIRST'

from src.core.Kernel import Kernel
from src.decorator.test_command import test_command
from src.decorator.option import option
from src.const.globals import COMMAND_TYPE_SERVICE


@test_command(command_type=COMMAND_TYPE_SERVICE)
@option('--option', '-o', is_flag=True, required=False,
        help="A first option as flag")
@option('--another-option', '-ao', is_flag=True, required=False,
        help="Another option")
def test__demo_command__first(kernel: Kernel, service: str, option=None, another_option=None):
    return 'FIRST'

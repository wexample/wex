from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option


@command()
@option('--option', '-o', is_flag=True, required=False,
        help="A first option as flag")
@option('--another-option-second', '-aos', is_flag=True, required=False,
        help="Another option")
def test__demo_command__second(kernel: Kernel, option=None, another_option_second=None):
    return 'SECOND'

from src.core.Kernel import Kernel
from src.decorator.test_command import test_command
from src.decorator.option import option


@test_command()
@option('--option', '-o', is_flag=True, required=False,
        help="A first option as flag")
@option('--another-option', '-ao', is_flag=True, required=False,
        help="Another option")
def test_2__another_demo_command__test(kernel: Kernel, option=None, another_option=None):
    return 'FIRST'

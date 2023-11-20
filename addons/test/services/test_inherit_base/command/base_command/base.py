from src.core.Kernel import Kernel
from src.decorator.test_command import test_command
from src.decorator.option import option
from src.const.globals import COMMAND_TYPE_SERVICE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@test_command(command_type=COMMAND_TYPE_SERVICE)
@option('--option', '-o', type=str, required=False,
        help="An option as flag")
def test_inherit_base__base_command__base(kernel: 'Kernel', service: str, option: str = None):
    return f'BASE:{option}:{service}'

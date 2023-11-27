from typing import TYPE_CHECKING

from src.decorator.alias import alias
from src.decorator.test_command import test_command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@alias('this-is-a-test-alias')
@test_command()
def test__demo_command__alias(kernel: 'Kernel'):
    return 'ALIAS'

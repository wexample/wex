from src.decorator.command import command
from src.decorator.alias import alias
from src.core import Kernel


@command()
@alias(name='this-is-a-test-alias')
def test__demo_command__alias(kernel: Kernel):
    return 'ALIAS'

from src.decorator.test_command import test_command
from src.decorator.alias import alias
from src.core import Kernel

@test_command()
@alias('this-is-a-test-alias')
def test__demo_command__alias(kernel: Kernel):
    return 'ALIAS'

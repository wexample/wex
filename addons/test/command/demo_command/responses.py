from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.decorator.test_command import test_command
from src.decorator.option import option
from src.core import Kernel

RESPONSES_DEFAULT_VALUES = {
    'string': 'STRING',
    'integer': 'INTEGER',
    'boolean': 'BOOLEAN',
}


@test_command()
@option('--type', '-t', required=True,
        help="Response type to test")
def test__demo_command__responses(kernel: Kernel, type: str):
    if type in RESPONSES_DEFAULT_VALUES:
        return RESPONSES_DEFAULT_VALUES[type]
    elif type == 'function':
        return _test__demo_command__responses_one
    elif type == 'shell':
        return InteractiveShellCommandResponse(kernel, ['ls', '-la'])


def _test__demo_command__responses_one(kernel: Kernel):
    return 'one'


def _test__demo_command__responses_two(kernel: Kernel, from_one: str):
    return from_one + '+two'

from typing import TYPE_CHECKING

from src.core.response.NonInteractiveShellCommandResponse import \
    NonInteractiveShellCommandResponse
from src.decorator.option import option
from src.decorator.test_command import test_command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


RESPONSES_DEFAULT_VALUES = {
    'string': 'STRING',
    'integer': 'INTEGER',
    'boolean': 'BOOLEAN',
}

@test_command()
@option('--type', '-t', required=True,
        help="Response type to test")
def test__demo_command__responses(kernel: 'Kernel', type: str):
    if type in RESPONSES_DEFAULT_VALUES:
        return RESPONSES_DEFAULT_VALUES[type]
    elif type == 'function':
        return _test__demo_command__responses_one
    elif type == 'shell':
        return NonInteractiveShellCommandResponse(kernel, ['ls', '-la'])


def _test__demo_command__responses_one():
    return 'one'


def _test__demo_command__responses_two(from_one: str):
    return from_one + '+two'

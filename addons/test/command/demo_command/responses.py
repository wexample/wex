from src.core.response.ShellCommandResponse import ShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.test_command import test_command
from src.core import Kernel


@test_command()
def test__demo_command__responses(kernel: Kernel):
    return ResponseCollectionResponse(kernel, [
        # Will be converted to PythonFunctionResponse
        _test__demo_command__responses_one,
        _test__demo_command__responses_two,
        ShellCommandResponse(kernel, ['ls', '-la', '{__prev__}'])
    ])


def _test__demo_command__responses_one():
    return 'one'


def _test__demo_command__responses_two():
    return 'two'

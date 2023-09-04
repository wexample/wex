from src.core.response.ShellCommandResponse import ShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.test_command import test_command
from src.decorator.response_collection import response_collection
from src.core import Kernel


@test_command()
@response_collection()
def test__demo_command__response_collection(kernel: Kernel, response_collection_step: int = None):
    return ResponseCollectionResponse(kernel, [
        'free-text',
        123,
        # Will be converted to FunctionResponse
        _test__demo_command__response_collection_one,
        _test__demo_command__response_collection_two,
        # ShellCommandResponse(kernel, ['ls', '-la', '{__prev__[2]}'])
    ])


def _test__demo_command__response_collection_one():
    return 'one'


def _test__demo_command__response_collection_two():
    return []

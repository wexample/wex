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
        _test__demo_command__response_collection_three,
        ShellCommandResponse(kernel, ['ls', '-la'])
    ])


def _test__demo_command__response_collection_one(
        kernel: Kernel,
        previous:int):
    return 'one'


def _test__demo_command__response_collection_two(
        kernel: Kernel,
        previous: str):
    return {
        'old': previous,
        'new': 'two'
    }


def _test__demo_command__response_collection_three(
        kernel: Kernel,
        previous: dict = None):
    return {
        'type': type(previous),
        'length': len(previous)
    }

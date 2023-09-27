from src.core.response.ShellCommandResponse import ShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.test_command import test_command
from src.core import Kernel


@test_command()
def test__demo_command__response_collection(kernel: Kernel):
    def _test__demo_command__response_collection_one(previous: int):
        return 'one'

    def _test__demo_command__response_collection_two(previous: str):
        return {
            'old': previous,
            'new': 'two'
        }

    def _test__demo_command__response_collection_three(previous: dict = None):
        return {
            'type': type(previous),
            'length': len(previous)
        }

    return ResponseCollectionResponse(kernel, [
        'free-text',
        123,
        # Will be converted to FunctionResponse
        _test__demo_command__response_collection_one,
        _test__demo_command__response_collection_two,
        _test__demo_command__response_collection_three,
        ShellCommandResponse(kernel, ['ls', '-la'])
    ])

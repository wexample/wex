from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.test_command import test_command
from src.core import Kernel


@test_command()
def test__demo_command__response_collection_three(kernel: Kernel):
    def _test__demo_command__response_collection_three_one(previous: int):
        return 'this-is-a-function-THREE'

    return ResponseCollectionResponse(kernel, [
        'this-is-a-test-THREE',
        InteractiveShellCommandResponse(kernel, ['echo', '"THREE"']),
        _test__demo_command__response_collection_three_one
    ])

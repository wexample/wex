from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.test_command import test_command
from src.core import Kernel

TEST_DEMO_COMMAND_THREE_RESULT_ONE = '____this-is-a-test-THREE'
TEST_DEMO_COMMAND_THREE_RESULT_SHELL = '____THREE'
TEST_DEMO_COMMAND_THREE_RESULT_FUNCTION = '____this-is-a-function-THREE'


@test_command()
def test__demo_command__response_collection_three(kernel: Kernel):
    def _test__demo_command__response_collection_three_one(previous: int):
        return TEST_DEMO_COMMAND_THREE_RESULT_FUNCTION

    return ResponseCollectionResponse(kernel, [
        TEST_DEMO_COMMAND_THREE_RESULT_ONE,
        InteractiveShellCommandResponse(kernel, ['echo', f'"{TEST_DEMO_COMMAND_THREE_RESULT_SHELL}"']),
        _test__demo_command__response_collection_three_one
    ])
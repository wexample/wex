from src.core.response.ResponseCollectionStopResponse import ResponseCollectionStopResponse
from src.core.response.AbortResponse import AbortResponse
from src.core.response.NonInteractiveShellCommandResponse import NonInteractiveShellCommandResponse
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.test_command import test_command
from src.core import Kernel
from src.decorator.option import option

TEST_DEMO_COMMAND_THREE_RESULT_ONE = '....THREE:simple-text'
TEST_DEMO_COMMAND_THREE_RESULT_SHELL = '....THREE:shell-response'
TEST_DEMO_COMMAND_THREE_RESULT_FUNCTION = '....THREE:function-response-text'


@test_command()
@option('--abort', '-a', is_flag=True, required=False, help="Ask to abort")
def test__demo_command__response_collection_three(kernel: Kernel, abort: bool = False):
    def _test__demo_command__response_collection_three_one():
        nonlocal abort

        if abort:
            return AbortResponse(kernel, 'TEST ABORT')

        return TEST_DEMO_COMMAND_THREE_RESULT_FUNCTION

    return ResponseCollectionResponse(kernel, [
        _test__demo_command__response_collection_three_one,
        TEST_DEMO_COMMAND_THREE_RESULT_ONE,
        InteractiveShellCommandResponse(kernel, ['echo', f'"{TEST_DEMO_COMMAND_THREE_RESULT_SHELL}"']),
    ])

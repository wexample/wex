from addons.core.command.check.hi import core__check__hi
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.test_command import test_command
from src.core import Kernel
from addons.test.command.demo_command.response_collection_three import test__demo_command__response_collection_three

TEST_DEMO_COMMAND_TWO_RESULT_FIRST = '..TWO:simple-text'
TEST_DEMO_COMMAND_TWO_RESULT_SHELL = '..TWO:shell-response'


@test_command()
def test__demo_command__response_collection_two(kernel: Kernel):
    def _test__demo_command__response_collection_two__simple_function(previous: int):
        return f'..TWO:simple-function-previous-value:{previous}'

    def _test__demo_command__response_collection_two__run_another_collection(previous: int = None):
        # This run will return unused response.
        kernel.run_function(
            core__check__hi,
        )

        return kernel.run_function(
            test__demo_command__response_collection_three,
        )

    def _test__demo_command__response_collection_three_command(previous):
        return InteractiveShellCommandResponse(kernel, ['echo', '..TWO:interactive-shell-response'])

    return ResponseCollectionResponse(kernel, [
        TEST_DEMO_COMMAND_TWO_RESULT_FIRST,
        f'{TEST_DEMO_COMMAND_TWO_RESULT_FIRST}(2)',
        _test__demo_command__response_collection_two__simple_function,
        InteractiveShellCommandResponse(kernel, ['echo', f'"{TEST_DEMO_COMMAND_TWO_RESULT_SHELL}"']),
        _test__demo_command__response_collection_two__simple_function,
        _test__demo_command__response_collection_two__run_another_collection,
        _test__demo_command__response_collection_three_command,
    ])

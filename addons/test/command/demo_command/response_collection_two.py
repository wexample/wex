from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.test_command import test_command
from src.core import Kernel
from addons.test.command.demo_command.response_collection_three import test__demo_command__response_collection_three


@test_command()
def test__demo_command__response_collection_two(kernel: Kernel):
    def _test__demo_command__response_collection_two_one(previous: int):
        return f'__Previous TWO value is : {previous}'

    def _test__demo_command__response_collection_three_nested(previous: int = None):
        return kernel.run_function(
            test__demo_command__response_collection_three,
        )

    return ResponseCollectionResponse(kernel, [
        '__this-is-a-test-TWO',
        '__this-is-a-test-TWO(2)',
        '__this-is-a-test-TWO(3)',
        InteractiveShellCommandResponse(kernel, ['echo', '"__TWO"']),
        _test__demo_command__response_collection_two_one,
        _test__demo_command__response_collection_three_nested
    ])

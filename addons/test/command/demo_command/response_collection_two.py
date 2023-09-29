from src.core.response.ShellCommandResponse import ShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.test_command import test_command
from src.core import Kernel
from addons.test.command.demo_command.response_collection_three import test__demo_command__response_collection_three


@test_command()
def test__demo_command__response_collection_two(kernel: Kernel):
    def _test__demo_command__response_collection_two_one(previous: int):
        return f'Previous TWO value is : {previous}'

    def _test__demo_command__response_collection_three_nested(previous: int = None):
        return kernel.run_function(
            test__demo_command__response_collection_three,
        )

    return ResponseCollectionResponse(kernel, [
        'this-is-a-test-TWO',
        'this-is-a-test-TWO(2)',
        'this-is-a-test-TWO(3)',
        ShellCommandResponse(kernel, ['echo', '"TWO"']),
        _test__demo_command__response_collection_two_one,
        _test__demo_command__response_collection_three_nested
    ])

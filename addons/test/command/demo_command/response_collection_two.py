from src.core.response.ShellCommandResponse import ShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.test_command import test_command
from src.core import Kernel
from addons.test.command.demo_command.response_collection_three import test__demo_command__response_collection_three


@test_command()
def test__demo_command__response_collection_two(kernel: Kernel):
    def _test__demo_command__response_collection_two_one(previous: int):
        return 'this-is-a-function-TWO'

    def _test__demo_command__response_collection_three_nested(previous: int):
        return kernel.run_function(
            test__demo_command__response_collection_three,
        )

    return ResponseCollectionResponse(kernel, [
        'this-is-a-test-TWO',
        # ShellCommandResponse(kernel, ['echo', '"TWO"']),
        # _test__demo_command__response_collection_two_one,
        # _test__demo_command__response_collection_three_nested
    ])

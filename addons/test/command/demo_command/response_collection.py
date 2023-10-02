from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.core.response.NonInteractiveShellCommandResponse import NonInteractiveShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.test_command import test_command
from src.core import Kernel
from addons.test.command.demo_command.response_collection_two import test__demo_command__response_collection_two

TEST_DEMO_COMMAND_RESULT_ONE = 'one'


@test_command()
def test__demo_command__response_collection(kernel: Kernel):
    def _test__demo_command__response_collection_one(previous: int):
        return TEST_DEMO_COMMAND_RESULT_ONE

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

    def _test__demo_command__response_collection_deeper(previous):
        def _test__demo_command__response_collection_deeper_two(previous):
            return {
                'passed': previous
            }

        return ResponseCollectionResponse(kernel, [
            '__sub-collection-free-text',
            '__sub-2',
            '__sub-3',
            '__sub-4',
            45600,
            # Will be converted to FunctionResponse
            _test__demo_command__response_collection_one,
            NonInteractiveShellCommandResponse(kernel, ['echo', 'will-be-passed-to-next-function']),
            _test__demo_command__response_collection_deeper_two
        ])

    def _test__demo_command__response_collection_run_another_collection(previous: dict = None):
        return kernel.run_function(
            test__demo_command__response_collection_two,
        )

    return ResponseCollectionResponse(kernel, [
        'free-text',
        'free-text-2',
        123,
        # Will be converted to FunctionResponse
        _test__demo_command__response_collection_one,
        _test__demo_command__response_collection_two,
        _test__demo_command__response_collection_three,
        NonInteractiveShellCommandResponse(kernel, ['ls', '-la']),
        'free-text-after-shell',
        _test__demo_command__response_collection_deeper,
        _test__demo_command__response_collection_deeper,
        _test__demo_command__response_collection_deeper,
        _test__demo_command__response_collection_run_another_collection,
        _test__demo_command__response_collection_run_another_collection,
        _test__demo_command__response_collection_run_another_collection,
        'last-text'
    ])

from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.core.response.NonInteractiveShellCommandResponse import NonInteractiveShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.test_command import test_command
from src.core import Kernel
from addons.test.command.demo_command.response_collection_two import test__demo_command__response_collection_two

TEST_DEMO_COMMAND_RESULT_FIRST_FUNCTION = 'function-response-text'


@test_command()
def test__demo_command__response_collection(kernel: Kernel):
    def _test__demo_command__response_collection__first_function(previous: int):
        return TEST_DEMO_COMMAND_RESULT_FIRST_FUNCTION

    def _test__demo_command__response_collection__second_function(previous: str):
        return {
            'old': previous,
            'new': 'two'
        }

    def _test__demo_command__response_collection__function_three(previous: dict = None):
        return {
            'type': type(previous),
            'length': len(previous)
        }

    def _test__demo_command__response_collection__sub_collection(previous):
        def callback(previous):
            return {
                'passed': previous
            }

        return ResponseCollectionResponse(kernel, [
            '--sub-collection:simple-text',
            '--sub-collection:simple-text-2',
            45600,
            456.00,
            # Will be converted to FunctionResponse
            _test__demo_command__response_collection__first_function,
            NonInteractiveShellCommandResponse(kernel, ['echo', '--sub-collection-shell:simple-text']),
            callback
        ])

    def _test__demo_command__response_collection__run_another_collection(previous: dict = None):
        return kernel.run_function(
            test__demo_command__response_collection_two,
        )

    return ResponseCollectionResponse(kernel, [
        'simple-response-text',
        'simple-response-text-2',
        123456,
        123.456,
        ['simple-list', 'simple-list'],
        {'simple-dict': True},
        # Will be converted to FunctionResponse
        _test__demo_command__response_collection__first_function,
        _test__demo_command__response_collection__second_function,
        _test__demo_command__response_collection__function_three,
        NonInteractiveShellCommandResponse(kernel, ['ls', '-la']),
        'free-text-after-shell',
        _test__demo_command__response_collection__sub_collection,
        _test__demo_command__response_collection__sub_collection,
        _test__demo_command__response_collection__sub_collection,
        _test__demo_command__response_collection__run_another_collection,
        _test__demo_command__response_collection__run_another_collection,
        _test__demo_command__response_collection__run_another_collection,
        'last-text'
    ])

from src.core.response.ResponseCollectionHiddenResponse import ResponseCollectionHiddenResponse
from src.core.response.NonInteractiveShellCommandResponse import NonInteractiveShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.test_command import test_command
from src.core import Kernel
from src.decorator.option import option
from addons.test.command.demo_command.response_collection_two import test__demo_command__response_collection_two

TEST_DEMO_COMMAND_RESULT_FIRST_FUNCTION = 'function-response-text'


@test_command()
@option('--abort', '-a', is_flag=True, required=False, help="Ask to abort")
def test__demo_command__response_collection(kernel: Kernel, abort: bool = False):
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

    def _test__demo_command__response_collection__sub_function_shell(previous):
        return NonInteractiveShellCommandResponse(
            kernel,
            ['echo', '--sub-function-shell:' + previous[0]])

    def _test__demo_command__response_collection__callback_hidden_response(previous):
        return ResponseCollectionHiddenResponse(
            kernel,
            previous + '-has-been-passed-to-hidden'
        )

    def _test__demo_command__response_collection__previous(previous: str):
        return previous + '-and-returned-by-next'

    def _test__demo_command__response_collection__sub_collection(previous):
        def callback(previous):
            return {
                'passed': previous
            }

        return ResponseCollectionResponse(kernel, [
            '--sub-collection-in-function:simple-text',
            '--sub-collection-in-function:simple-text-2',
            45600,
            456.00,
            # Will be converted to FunctionResponse
            _test__demo_command__response_collection__first_function,
            NonInteractiveShellCommandResponse(kernel, ['echo', '--sub-collection-shell:simple-text']),
            callback
        ])

    def _test__demo_command__response_collection__run_another_collection(previous: dict = None):
        nonlocal abort

        return kernel.run_function(
            test__demo_command__response_collection_two,
            {
                'abort': abort
            }
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
        NonInteractiveShellCommandResponse(kernel, ['echo', 'shell-text']),
        _test__demo_command__response_collection__sub_function_shell,
        'free-text-after-shell',
        _test__demo_command__response_collection__callback_hidden_response,
        _test__demo_command__response_collection__previous,
        ResponseCollectionResponse(kernel, [
            '--sub-collection-direct:simple-text'
        ]),
        _test__demo_command__response_collection__run_another_collection,
        _test__demo_command__response_collection__run_another_collection,
        _test__demo_command__response_collection__sub_collection,
        _test__demo_command__response_collection__sub_collection,
        'last-text'
    ])

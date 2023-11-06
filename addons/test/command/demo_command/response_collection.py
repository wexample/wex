from src.core.response.HiddenResponse import HiddenResponse
from src.core.response.NonInteractiveShellCommandResponse import NonInteractiveShellCommandResponse
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.decorator.test_command import test_command
from src.core import Kernel
from src.decorator.option import option
from addons.test.command.demo_command.response_collection_two import test__demo_command__response_collection_two
from addons.test.command.demo_command.counting_collection import test__demo_command__counting_collection

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
            'type': str(type(previous)),
            'length': len(previous)
        }

    def _test__demo_command__response_collection__sub_function_shell(previous):
        return NonInteractiveShellCommandResponse(
            kernel,
            ['echo', '--sub-function-shell:' + previous[0]])

    def _test__demo_command__response_collection__callback_hidden_response(previous):
        return HiddenResponse(
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

        return QueuedCollectionResponse(kernel, [
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

    def _test__demo_command__response_collection__counting_collection(previous=None):
        kernel.io.log('Previous : ' + str(previous))

        error = None
        if previous != '__previous__':
            error: True

        response = kernel.run_function(
            test__demo_command__counting_collection,
            {
                'initial': 1000
            }
        )

        rendered = response.print()

        if error:
            kernel.io.error(
                'ERR_UNEXPECTED',
                {
                    'error': f'Bad previous to response match : previous : {previous}, rendered : {rendered}'
                }
            )
        return response

    return QueuedCollectionResponse(kernel, [
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
        QueuedCollectionResponse(kernel, [
            '--sub-collection-direct:simple-text',
        ]),
        _test__demo_command__response_collection__run_another_collection,
        _test__demo_command__response_collection__run_another_collection,
        _test__demo_command__response_collection__sub_collection,
        _test__demo_command__response_collection__sub_collection,
        '__previous__',
        _test__demo_command__response_collection__counting_collection,
        _test__demo_command__response_collection__counting_collection,
        'last-text'
    ])

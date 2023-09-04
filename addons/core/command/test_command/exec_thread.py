from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.test_command import test_command
from src.decorator.command import command
from src.core import Kernel


@command()
@test_command
def core__test_command__exec_thread(kernel: Kernel):
    return ResponseCollectionResponse([
        # Will be converted to PythonFunctionResponse
        _core__test_command__exec_thread_one,
        _core__test_command__exec_thread_two,
        # ShellCommandResponse(['ls', '-la', '{__prev__}'])
    ])


def _core__test_command__exec_thread_one():
    return 'one'


def _core__test_command__exec_thread_two():
    return 'two'

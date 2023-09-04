from src.core.response.ExecThreadResponse import ExecThreadResponse
from src.decorator.test_command import test_command
from src.decorator.command import command
from src.core import Kernel


@command()
@test_command
def core__test_command__exec_thread(kernel: Kernel):
    return ExecThreadResponse([
        _core__test_command__exec_thread_one,
        _core__test_command__exec_thread_two
    ])


def _core__test_command__exec_thread_one():
    return 'one'


def _core__test_command__exec_thread_two():
    return 'two'

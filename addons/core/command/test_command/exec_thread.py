from src.decorator.test_command import test_command
from src.decorator.command import command
from src.core import Kernel


@command()
@test_command
def core__test_command__exec_thread(kernel: Kernel):
    return True

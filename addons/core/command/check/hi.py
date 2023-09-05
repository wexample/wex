from src.decorator.command import command
from src.decorator.alias import alias
from src.core import Kernel


@command(help="Return hi! Used to check if core vitals are working")
@alias('hi')
def core__check__hi(kernel: Kernel):
    return 'hi!'

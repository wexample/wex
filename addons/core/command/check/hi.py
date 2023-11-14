from src.decorator.command import command
from src.decorator.alias import alias
from src.core import Kernel


@alias('hi')
@command(help="Return hi! Used to check if core vitals are working")
def core__check__hi(kernel: Kernel):
    return 'hi!'

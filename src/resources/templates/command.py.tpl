import click

from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel


@command()
@option('--arg', '-a', type=str, required=True, help="Argument")
def {function_name}(kernel: Kernel, arg):
    pass

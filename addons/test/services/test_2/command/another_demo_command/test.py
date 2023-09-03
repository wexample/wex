import click

from src.core.Kernel import Kernel
from src.decorator.command import command


@command()
@click.option('--option', '-o', is_flag=True, required=False,
              help="A first option as flag")
@click.option('--another-option', '-ao', is_flag=True, required=False,
              help="Another option")
def test_2__another_demo_command__test(kernel: Kernel, option=None, another_option=None):
    return 'FIRST'

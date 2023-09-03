import click

from src.core.Kernel import Kernel
from src.decorator.command import command


@command()
@click.option('--option', '-o', is_flag=True, required=False,
              help="A first option as flag")
@click.option('--another-option', '-ao', is_flag=True, required=False,
              help="Another option")
def test__demo_command__first(kernel: Kernel, option=None, another_option=None):
    return 'FIRST'

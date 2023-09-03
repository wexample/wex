import click

from src.core.Kernel import Kernel
from src.decorator.command import command


@command()
@click.option('--local-option', '-lo', required=False)
def app__local_command__test(kernel: Kernel, local_option: str):
    return f'OK:{local_option}'

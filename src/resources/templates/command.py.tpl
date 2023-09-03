from src.decorator.command import command
from src.core import Kernel


@command()
@click.option('--arg', '-a', type=str, required=True, help="Argument")
def {function_name}(kernel: Kernel, arg):
    pass

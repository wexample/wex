from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel
from src.const.globals import {command_type_constant}


@command(help="Description", command_type={command_type_constant})
@option('--arg', '-a', type=str, required=True, help="Argument")
def {function_name}(kernel: Kernel, arg):
    pass

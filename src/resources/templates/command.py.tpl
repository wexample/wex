from src.decorator.command import command
from src.decorator.option import option
from src.core import Kernel
from src.const.globals import {command_type_constant}


@command(help="Description", command_type={command_type_constant})
@option('--option', '-o', type=str, required=True, help="Option")
def {function_name}(kernel: Kernel, option):
    pass

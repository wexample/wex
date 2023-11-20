from src.decorator.command import command
from src.decorator.option import option
from src.const.globals import COMMAND_TYPE_APP
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="An app test command", command_type=COMMAND_TYPE_APP)
@option('--local-option', '-lo', required=False)
def app__local_command__test(kernel: 'Kernel', local_option: str):
    return f'OK:{local_option}'

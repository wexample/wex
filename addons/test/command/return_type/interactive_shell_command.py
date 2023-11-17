from src.decorator.command import command
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse


@command(help="Return an int value", command_type=COMMAND_TYPE_ADDON)
def test__return_type__interactive_shell_command(kernel: Kernel):
    return InteractiveShellCommandResponse(kernel, [
        'echo', 'INTERACTIVE_SHELL_COMMAND_RESPONSE'
    ])

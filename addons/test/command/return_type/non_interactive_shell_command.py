from src.decorator.command import command
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON
from src.core.response.NonInteractiveShellCommandResponse import NonInteractiveShellCommandResponse


@command(help="Return an int value", command_type=COMMAND_TYPE_ADDON)
def test__return_type__non_interactive_shell_command(kernel: Kernel):
    return NonInteractiveShellCommandResponse(kernel, [
        'echo', 'NON_INTERACTIVE_SHELL_COMMAND_RESPONSE'
    ])
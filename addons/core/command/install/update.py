from src.decorator.command import command
from src.core import Kernel
from src.const.globals import COMMAND_TYPE_ADDON, CORE_COMMAND_NAME
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.decorator.as_sudo import as_sudo


@as_sudo()
@command(help="Description", command_type=COMMAND_TYPE_ADDON)
def core__install__update(kernel: Kernel):
    return InteractiveShellCommandResponse(kernel, [
        'sudo',
        'apt',
        'update',
        '&&',
        'sudo',
        'apt',
        'install',
        '--only-upgrade',
        CORE_COMMAND_NAME,
    ])

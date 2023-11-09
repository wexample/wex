from src.helper.command import command_to_string, internal_command_to_shell
from src.const.globals import VERBOSITY_LEVEL_MAXIMUM


def process_post_exec(
        kernel,
        command: []):
    kernel.io.log(
        'Queuing shell command : ' + command_to_string(command),
        verbosity=VERBOSITY_LEVEL_MAXIMUM
    )
    kernel.post_exec.append(command)


def process_post_exec_function(kernel, internal_command: str, args: None | list = None, is_async=False):
    command = internal_command_to_shell(
        kernel=kernel,
        internal_command=internal_command,
        args=args
    )

    if is_async:
        command.insert(0, 'nohup')
        command += ['>', '/dev/null', '2>&1', '&']

    process_post_exec(
        kernel,
        command
    )

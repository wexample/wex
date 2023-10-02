from src.helper.command import command_to_string, core_call_to_shell_command
from src.const.globals import VERBOSITY_LEVEL_MAXIMUM


def process_post_exec(
        kernel,
        command: []):
    kernel.log(
        'Queuing shell command : ' + command_to_string(command),
        verbosity=VERBOSITY_LEVEL_MAXIMUM
    )
    kernel.post_exec.append(command)


def process_post_exec_wex(kernel, function: callable, args: dict = {}, is_async=False):
    command = core_call_to_shell_command(
        kernel,
        function,
        args
    )

    if is_async:
        command.insert(0, 'nohup')
        command += ['>', '/dev/null', '2>&1', '&']

    process_post_exec(
        kernel,
        command
    )

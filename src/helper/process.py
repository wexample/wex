from src.helper.command import command_to_string
from src.const.globals import COMMAND_TYPE_ADDON, VERBOSITY_LEVEL_QUIET, VERBOSITY_LEVEL_MEDIUM, VERBOSITY_LEVEL_MAXIMUM
from src.helper.args import convert_dict_to_args


def process_post_exec(kernel, command: []):
    kernel.log(
        'Queuing shell command : ' + command_to_string(command),
        verbosity=VERBOSITY_LEVEL_MAXIMUM
    )
    kernel.post_exec.append(command)


def process_post_exec_wex(kernel, function: callable, args: dict = {}, is_async=False):
    command = ([
                   'bash',
                   kernel.path['core.cli'],
                   kernel.get_command_resolver(COMMAND_TYPE_ADDON).build_command_from_function(function),
               ]
               + convert_dict_to_args(function, args)
               + [
                   '--kernel-task-id',
                   kernel.task_id
               ])

    if kernel.current_request.verbosity == VERBOSITY_LEVEL_QUIET:
        command += ['--quiet']
    elif kernel.current_request.verbosity == VERBOSITY_LEVEL_MEDIUM:
        command += ['--vv']
    elif kernel.current_request.verbosity == VERBOSITY_LEVEL_MAXIMUM:
        command += ['--vvv']

    if is_async:
        command.insert(0, 'nohup')
        command += ['>', '/dev/null', '2>&1', '&']

    process_post_exec(
        kernel,
        command
    )

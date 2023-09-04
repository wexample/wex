
from src.helper.command import command_to_string
from src.const.globals import COMMAND_TYPE_ADDON
from src.helper.args import convert_dict_to_args


def process_post_exec(kernel, command: []):
    kernel.log('Queuing shell command : ' + command_to_string(command))

    kernel.post_exec.append(command)


def process_post_exec_wex(kernel, function: callable, args: dict = {}, is_async=False):
    command = [
                  'bash',
                  kernel.path['core.cli'],
                  kernel.get_command_resolver(COMMAND_TYPE_ADDON).build_command_from_function(function),
              ] + convert_dict_to_args(function, args)

    if is_async:
        command.insert(0, 'nohup')
        command += ['>', '/dev/null', '2>&1', '&']

    process_post_exec(
        kernel,
        command
    )

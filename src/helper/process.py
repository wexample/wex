import os

from src.helper.command import command_to_string
from src.const.globals import COMMAND_TYPE_ADDON
from src.helper.args import convert_dict_to_args
from src.helper.file import set_user_or_sudo_user_owner


def process_post_exec(kernel, command: []):
    post_exec_file_path = os.path.join(kernel.path['tmp'], 'process', str(kernel.process_id) + '.post-exec')

    command_string = command_to_string(command)
    kernel.log('Queuing shell command : ' + command_string)
    # Print joined command in a post process file.
    with open(post_exec_file_path, 'a') as f:
        f.write(command_string + '\n')

    set_user_or_sudo_user_owner(post_exec_file_path)


def process_post_exec_wex(kernel, function: callable, args: dict = {}, is_async=False):
    command = [
                  'bash',
                  kernel.path['core.cli'],
                  kernel.create_command_processor(COMMAND_TYPE_ADDON).build_command_from_function(function),
              ] + convert_dict_to_args(function, args)

    if is_async:
        command.insert(0, 'nohup')
        command += ['>', '/dev/null', '2>&1', '&']

    process_post_exec(
        kernel,
        command
    )

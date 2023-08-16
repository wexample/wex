import os

from src.helper.args import convert_dict_to_args
from src.helper.command import build_command_from_function
from src.helper.file import set_owner
from src.helper.system import get_sudo_username


def process_post_exec(kernel, args):
    post_exec_file_path = os.path.join(kernel.path['tmp'], 'process', str(kernel.process_id) + '.post-exec')

    # Print joined command in a post process file.
    with open(post_exec_file_path, 'a') as f:
        f.write(
            ' '.join(['"' + arg + '"' if ' ' in arg else arg for arg in args])
            + '\n'
        )

    # Post exec file will be removed after execution,
    # so we need to give proper user permission to do it.
    sudo_user = get_sudo_username()
    if sudo_user:
        set_owner(post_exec_file_path, sudo_user)


def process_post_exec_wex(kernel, function: callable, args={}, is_async=False):
    command = [
                  'bash',
                  kernel.path['core.cli'],
                  build_command_from_function(function),
              ] + convert_dict_to_args(function, args)

    if is_async:
        command.insert(0, 'nohup')
        command += ['>', '/dev/null', '2>&1', '&']

    process_post_exec(
        kernel,
        command
    )

import subprocess

from src.helper.file import create_file_path
from src.core.IOManager import IO_DEFAULT_LOG_LENGTH
from src.const.globals import VERBOSITY_LEVEL_QUIET, VERBOSITY_LEVEL_MEDIUM, VERBOSITY_LEVEL_MAXIMUM


def internal_command_to_shell(kernel, internal_command: str, args: None | list = None) -> list:
    command = ([
                   'bash',
                   kernel.get_path('core.cli'),
                   internal_command
               ]
               + (args or [])
               + [
                   '--kernel-task-id',
                   kernel.task_id
               ])

    if kernel.verbosity == VERBOSITY_LEVEL_QUIET:
        command += ['--quiet']
    elif kernel.verbosity == VERBOSITY_LEVEL_MEDIUM:
        command += ['--vv']
    elif kernel.verbosity == VERBOSITY_LEVEL_MAXIMUM:
        command += ['--vvv']

    if kernel.io.log_length != IO_DEFAULT_LOG_LENGTH:
        command += [
            '--log-length',
            str(kernel.io.log_length)
        ]

    return command


def command_exists(command) -> bool:
    process = subprocess.Popen(
        'command -v ' + command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out_content, err_content = process.communicate()

    return out_content.decode() != ''


def execute_command_tree(kernel, command_tree, working_directory=None, async_mode=False, **kwargs):
    if isinstance(command_tree, list) and any(isinstance(i, list) for i in command_tree):
        # If the command_tree is a list and contains sub lists (nested commands)
        # We execute the innermost command first
        for i, sub_command in enumerate(command_tree):
            if isinstance(sub_command, list):
                # Recursive call to execute the nested command
                success, output = execute_command_tree(kernel, sub_command, working_directory, async_mode, **kwargs)

                if not success:
                    return success, output

                # Replace the nested command with the output of its execution
                command_tree[i:i + 1] = output

                # Now command_tree is a flat list with the results of the inner command included

    # Execute the modified (flattened) command_tree with the results of inner commands
    return execute_command(kernel, command_tree, working_directory, async_mode, **kwargs)


def execute_command(
        kernel,
        command: list | str,
        working_directory=None,
        async_mode=False,
        **kwargs):
    import subprocess
    import os

    if working_directory is None:
        working_directory = os.getcwd()

    command_str = command if isinstance(command, str) else command_to_string(command)
    kernel.io.log(f'Running shell command : {command_str}', verbosity=VERBOSITY_LEVEL_MAXIMUM)

    if async_mode:
        tmp_dir = os.path.join(kernel.get_or_create_path('tmp'), 'subprocess') + os.sep

        popen_args = {
            'cwd': working_directory,
            'start_new_session': True,
            'stdout': open(create_file_path(tmp_dir + kernel.task_id + '.stdout'), 'a'),
            'stderr': open(create_file_path(tmp_dir + kernel.task_id + '.stderr'), 'a'),
            **kwargs
        }

        return subprocess.Popen(
            command,
            **popen_args,
        )
    else:
        popen_args = {
            'cwd': working_directory,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.STDOUT,
            **kwargs
        }

        # If async mode is False, run the process in the current thread
        process = subprocess.Popen(command, **popen_args)
        out_content, _ = process.communicate()
        out_content_decoded: str = out_content.decode()
        success: bool = (process.returncode == 0)

        kernel.io.log(
            out_content_decoded,
            verbosity=VERBOSITY_LEVEL_MAXIMUM)

        return success, out_content_decoded.splitlines()


def command_escape(string: str, quote_char: str = '"') -> str:
    # Escape existing quotes
    item = string.replace(quote_char, '\\' + quote_char)
    # Add quotes around the item
    return quote_char + item + quote_char


def command_to_string(command: list | str):
    if isinstance(command, str):
        return command

    output = []

    for item in command:
        if isinstance(item, list):
            output.append(
                '$(' + command_to_string(item) + ')'
            )
        else:
            output.append(item)

    return ' '.join(output)


def is_same_command(command_a, command_b) -> bool:
    return command_a.callback.__name__ == command_b.callback.__name__

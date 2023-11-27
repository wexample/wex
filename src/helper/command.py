from __future__ import annotations

import os
import subprocess

from src.core.command.ScriptCommand import ScriptCommand
from src.helper.file import file_create_parent_dir
from src.core.IOManager import IO_DEFAULT_LOG_LENGTH
from src.const.globals import VERBOSITY_LEVEL_QUIET, VERBOSITY_LEVEL_MEDIUM, VERBOSITY_LEVEL_MAXIMUM
from typing import Any, List, Union, Tuple, Optional, Dict, NoReturn
from subprocess import Popen
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def internal_command_to_shell(kernel: 'Kernel', internal_command: str, args: None | list[str] = None) -> list[str]:
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


def command_exists(shell_command: str) -> bool:
    process = subprocess.Popen(
        'command -v ' + shell_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out_content, err_content = process.communicate()

    return out_content.decode() != ''


def execute_command_tree(
        kernel: 'Kernel',
        command_tree: List[Union[Any, str]],
        working_directory: str | None = None,
        ignore_error: bool = False,
        **kwargs: Any) -> Union[Popen[Any], Tuple[bool, List[str]]]:
    if isinstance(command_tree, list) and any(isinstance(i, list) for i in command_tree):
        # If the command_tree is a list and contains sub lists (nested commands)
        # We execute the innermost command first
        for i, sub_command in enumerate(command_tree):
            if isinstance(sub_command, list):
                # Recursive call to execute the nested command
                result = execute_command_tree(
                    kernel=kernel,
                    command_tree=sub_command,
                    working_directory=working_directory,
                    **kwargs)

                if not isinstance(result, Popen):
                    success, output = result

                    if not success:
                        return success, output

                    # Replace the nested command with the output of its execution
                    command_tree[i:i + 1] = output

                # Now command_tree is a flat list with the results of the inner command included

    # Execute the modified (flattened) command_tree with the results of inner commands
    return execute_command_sync(
        kernel=kernel,
        command=command_tree,
        working_directory=working_directory,
        ignore_error=ignore_error,
        **kwargs)


def execute_command_async(
        kernel: 'Kernel',
        command: Union[List[str], str],
        working_directory: Optional[str] = None,
        **kwargs: Any
) -> Popen[Any]:
    if working_directory is None:
        working_directory = os.getcwd()

    command_str = command_to_string(command)
    kernel.io.log(f'Running shell command : {command_str}', verbosity=VERBOSITY_LEVEL_MAXIMUM)

    tmp_dir = os.path.join(kernel.get_or_create_path('tmp'), 'subprocess') + os.sep

    popen_args = {
        'cwd': working_directory,
        'start_new_session': True,
        'stdout': open(file_create_parent_dir(tmp_dir + kernel.task_id + '.stdout'), 'a'),
        'stderr': open(file_create_parent_dir(tmp_dir + kernel.task_id + '.stderr'), 'a'),
        **kwargs
    }

    return subprocess.Popen(
        command,
        **popen_args,
    )


def execute_command_sync(
        kernel: 'Kernel',
        command: Union[List[str], str],
        working_directory: Optional[str] = None,
        ignore_error: bool = False,
        **kwargs: Any
) -> Tuple[bool, List[str]]:
    if working_directory is None:
        working_directory = os.getcwd()

    command_str = command_to_string(command)
    kernel.io.log(f'Running shell command : {command_str}', verbosity=VERBOSITY_LEVEL_MAXIMUM)

    popen_args = {
        'cwd': working_directory,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.STDOUT,
        **kwargs
    }

    process = subprocess.Popen(command, **popen_args)
    out_content, _ = process.communicate()
    out_content_decoded: str = out_content.decode()
    success: bool = (process.returncode == 0)

    if not success and not ignore_error:
        kernel.io.error(
            f'Error when running command : {command_to_string(command)}'
            + os.linesep + os.linesep
            + out_content_decoded)

    kernel.io.log(
        out_content_decoded,
        verbosity=VERBOSITY_LEVEL_MAXIMUM)

    return success, out_content_decoded.splitlines()


def command_escape(string: str, quote_char: str = '"') -> str:
    # Escape existing quotes
    escaped_string = string.replace('\\', '\\\\').replace(quote_char, '\\' + quote_char)
    # Add quotes around the escaped string
    return quote_char + escaped_string + quote_char


def command_to_string(command: List[str] | str) -> str:
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


def is_same_command(command_a: ScriptCommand, command_b: ScriptCommand) -> bool:
    if command_a.function.callback is not None and command_b.function.callback is not None:
        return command_a.function.callback.__name__ == command_b.function.callback.__name__
    return False


def apply_command_decorator(
        kernel: 'Kernel',
        function: Command,
        group: str,
        name: str,
        options: Optional[Dict[str, str]] = None) -> NoReturn | Any:
    if group in kernel.decorators and name in kernel.decorators[group]:
        decorator = kernel.decorators[group][name]
        options = options or {}

        return decorator(
            **options
        )(function)
    else:
        kernel.io.error(f'Missing decorator {group}.{name}')

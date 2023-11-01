import subprocess
import datetime
import os

from src.core.IOManager import IO_DEFAULT_LOG_LENGTH
from src.helper.args import convert_dict_to_args
from src.const.globals import COMMAND_TYPE_ADDON, VERBOSITY_LEVEL_QUIET, VERBOSITY_LEVEL_MEDIUM, VERBOSITY_LEVEL_MAXIMUM


def core_call_to_shell_command(kernel, function: callable, args: list | dict = {}) -> list:
    if isinstance(args, dict):
        args = convert_dict_to_args(function, args)

    command = ([
                   'bash',
                   kernel.get_path('core.cli'),
                   kernel.get_command_resolver(function.callback.command_type).build_command_from_function(function),
               ]
               + args
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


def execute_command(kernel, command: list | str, working_directory=None, async_mode=False, **kwargs):
    if working_directory is None:
        working_directory = os.getcwd()

    # Merge kwargs with existing arguments
    popen_args = {
        'cwd': working_directory,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.STDOUT,
        **kwargs  # This will overwrite existing keys with values from kwargs, if any
    }

    command_str = command if isinstance(command, str) else command_to_string(command)
    kernel.io.log(f'Running shell command : {command_str}', verbosity=VERBOSITY_LEVEL_MAXIMUM)
    process = subprocess.Popen(command, **popen_args)

    if async_mode:
        # Just return the process object, and the caller can decide what to do with it.
        return process
    else:
        out_content, _ = process.communicate()
        out_content_decoded: str = out_content.decode()
        success: bool = (process.returncode == 0)

        kernel.logger.write_output(out_content_decoded)
        kernel.io.log(out_content_decoded, verbosity=VERBOSITY_LEVEL_MAXIMUM)

        return success, out_content_decoded.splitlines()


def command_to_string(command: list | str, add_quotes: bool = True, quote_char: str = '"'):
    if isinstance(command, str):
        return command

    output = []

    for item in command:
        if isinstance(item, list):
            output.append(
                '$(' + command_to_string(item, add_quotes, quote_char) + ')'
            )
        else:
            if add_quotes and ' ' in item:
                # Escape existing quotes
                item = item.replace(quote_char, '\\' + quote_char)
                # Add quotes around the item
                output.append(quote_char + item + quote_char)
            else:
                output.append(item)

    return ' '.join(output)

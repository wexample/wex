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


def prepare_logs(kernel):
    date_now = datetime.date.today()
    date_formatted = date_now.strftime("%Y-%m-%d")

    os.makedirs(kernel.get_or_create_path('log'), exist_ok=True)

    out_path = os.path.join(kernel.get_or_create_path('log'), f"{date_formatted}-{kernel.task_id}.out")
    err_path = os.path.join(kernel.get_or_create_path('log'), f"{date_formatted}-{kernel.task_id}.err")

    return out_path, err_path


def execute_command(kernel, command: list | str, working_directory=None, async_mode=False, **kwargs):
    if working_directory is None:
        working_directory = os.getcwd()

    out_path, err_path = prepare_logs(kernel)

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
        success = (process.returncode == 0)

        # Log stdout (which now also includes stderr)
        with open(out_path, 'a') as out_file:
            out_file.write(out_content.decode())

        out_content_decoded = out_content.decode().splitlines()
        kernel.io.log(out_content, verbosity=VERBOSITY_LEVEL_MAXIMUM)

        return success, out_content_decoded


def command_to_string(command: list, add_quotes: bool = True, quote_char: str = '"'):
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

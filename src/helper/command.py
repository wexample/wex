from src.const.globals import (
    COMMAND_SEPARATOR_FUNCTION_PARTS, CORE_COMMAND_NAME, COMMAND_SEPARATOR_ADDON,
    COMMAND_SEPARATOR_GROUP,
)
from src.helper.args import convert_dict_to_args


def build_command_parts(function_name: callable) -> list:
    return function_name.split(COMMAND_SEPARATOR_FUNCTION_PARTS)[:3]


def build_command_from_function(function: callable) -> str:
    parts = build_command_parts(function.callback.__name__)
    return f'{parts[0]}{COMMAND_SEPARATOR_ADDON}{parts[1]}{COMMAND_SEPARATOR_GROUP}{parts[2]}'


def build_full_command_from_function(function: callable, args: dict = None) -> str:
    output = f'{CORE_COMMAND_NAME} '
    output += build_command_from_function(function) + ' '
    output += ' '.join(convert_dict_to_args(function, args))
    return output


def execute_command(kernel, command, working_directory=None, stdout=None, stderr=None):
    # Performance optimisation
    import datetime
    import os
    import subprocess

    if working_directory is None:
        working_directory = os.getcwd()

    if stderr is None:
        stderr = subprocess.STDOUT

    date_now = datetime.date.today()
    date_formatted = date_now.strftime("%Y-%m-%d")

    # Create a log file with the timestamp in its name
    out_path = os.path.join(kernel.path['log'], f"{date_formatted}-{kernel.process_id}.out")
    err_path = os.path.join(kernel.path['log'], f"{date_formatted}-{kernel.process_id}.err")

    os.makedirs(
        kernel.path['log'],
        exist_ok=True
    )

    with open(out_path, 'w') as out_file:
        with open(err_path, 'w') as err_file:
            return subprocess.Popen(
                command,
                cwd=working_directory,
                stdout=stdout or out_file,
                stderr=stderr or err_file,
            )

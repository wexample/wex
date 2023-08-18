import os
import re
import importlib.util

from addons.app.const.app import APP_DIR_APP_DATA
from src.helper.args import convert_dict_to_args
from src.const.globals import (
    COMMAND_PATTERN_ADDON,
    COMMAND_PATTERN_APP,
    COMMAND_PATTERN_CORE,
    COMMAND_PATTERN_SERVICE,
    COMMAND_PATTERN_USER,
    COMMAND_TYPE_ADDON,
    COMMAND_TYPE_APP,
    COMMAND_TYPE_CORE,
    COMMAND_TYPE_SERVICE,
    COMMAND_TYPE_USER, COMMAND_SEPARATOR_FUNCTION_PARTS, CORE_COMMAND_NAME, COMMAND_SEPARATOR_ADDON,
    COMMAND_SEPARATOR_GROUP,
)


def build_command_match(command: str):
    match = re.match(COMMAND_PATTERN_ADDON, command)
    if match:
        return match, COMMAND_TYPE_ADDON

    match = re.match(COMMAND_PATTERN_SERVICE, command)
    if match:
        return match, COMMAND_TYPE_SERVICE

    match = re.match(COMMAND_PATTERN_APP, command)
    if match:
        return match, COMMAND_TYPE_APP

    match = re.match(COMMAND_PATTERN_USER, command)
    if match:
        return match, COMMAND_TYPE_USER

    match = re.match(COMMAND_PATTERN_CORE, command)
    if match:
        return match, COMMAND_TYPE_CORE

    return None, None


def build_function_name_from_match(match: list, command_type: str) -> str:
    return f"{match.group(1)}{COMMAND_SEPARATOR_FUNCTION_PARTS}{match.group(2)}{COMMAND_SEPARATOR_FUNCTION_PARTS}{match.group(3)}"


def build_command_path_from_match(kernel, match, command_type: str, subdir: str = None) -> str | None:
    if command_type == COMMAND_TYPE_ADDON:
        base_path = f"{kernel.path['addons']}{match.group(1)}/"
        command_path = os.path.join(match.group(2), match.group(3))
    elif command_type == COMMAND_TYPE_APP:
        base_path = f"{kernel.addons['app']['path']['call_app_dir']}{APP_DIR_APP_DATA}"
        command_path = os.path.join(match[1], match[2])
    elif command_type == COMMAND_TYPE_SERVICE:
        base_path = f"{kernel.registry['services'][match[1]]['dir']}/"
        command_path = match[2]
    elif command_type == COMMAND_TYPE_USER:
        base_path = f"{os.path.expanduser('~')}/{APP_DIR_APP_DATA}"
        command_path = os.path.join(match[1], match[2])
    else:
        return None

    if subdir:
        base_path += f"{subdir}/"

    return os.path.join(base_path, 'command', command_path + '.py')


def get_function_from_match(kernel, match, command_type: str) -> str:
    command_path = build_command_path_from_match(kernel, match, command_type)

    # Import module and load function.
    spec = importlib.util.spec_from_file_location(command_path, command_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return getattr(
        module,
        build_function_name_from_match(match, command_type)
    )


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

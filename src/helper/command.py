import datetime
import os
import re
import subprocess
from src.helper.args import convert_dict_to_args

from src.const.globals import COMMAND_PATTERN, COMMAND_SEPARATOR_ADDON, COMMAND_SEPARATOR_GROUP, \
    COMMAND_SEPARATOR_FUNCTION_PARTS


def build_command_match(command: str):
    return re.match(COMMAND_PATTERN, command)


def build_function_name_from_match(match: list) -> str:
    return f"{match.group(1)}{COMMAND_SEPARATOR_FUNCTION_PARTS}{match.group(2)}{COMMAND_SEPARATOR_FUNCTION_PARTS}{match.group(3)}"


def build_command_parts(function_name: callable) -> list:
    return function_name.split(COMMAND_SEPARATOR_FUNCTION_PARTS)[:3]


def build_command_from_function(function: callable) -> str:
    parts = build_command_parts(function.callback.__name__)
    return f'{parts[0]}{COMMAND_SEPARATOR_ADDON}{parts[1]}{COMMAND_SEPARATOR_GROUP}{parts[2]}'


def build_full_command_from_function(function: callable, args: dict = None) -> str:
    output = build_command_from_function(function) + ' '
    output += ' '.join(convert_dict_to_args(function, args))
    return output


def execute_command(kernel, command, working_directory):
    date_now = datetime.date.today()
    date_formatted = date_now.strftime("%Y-%m-%d")

    # Create a log file with the timestamp in its name
    log_file = os.path.join(kernel.path['log'], f"{date_formatted}-{kernel.process_id}.log")

    os.makedirs(
        kernel.path['log'],
        exist_ok=True
    )

    with open(log_file, 'w') as file:
        subprocess.Popen(command, cwd=working_directory, stdout=file, stderr=subprocess.STDOUT)


def get_commands_groups_names(kernel, addon):
    group_names = set()

    if addon in kernel.registry['addons']:
        for command in kernel.registry['addons'][addon]['commands'].keys():
            group_name = command.split("::")[1].split("/")[0]
            group_names.add(group_name)
    return list(group_names)

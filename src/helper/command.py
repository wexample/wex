import re

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

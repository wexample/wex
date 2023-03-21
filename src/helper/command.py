import re

from src.const.globals import COMMAND_PATTERN


def build_command_match(command: str):
    return re.match(COMMAND_PATTERN, command)


def build_function_name_from_match(match) -> str:
    return f"{match.group(1)}_{match.group(2)}_{match.group(3)}"

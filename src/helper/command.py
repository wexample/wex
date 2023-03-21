import re

from src.const.globals import COMMAND_PATTERN


def build_command_match(command: str):
    return re.match(COMMAND_PATTERN, command)

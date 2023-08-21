import os

from src.helper.args import convert_dict_to_args
from src.const.globals import COMMAND_PATTERN_ADDON, COMMAND_TYPE_ADDON, COMMAND_SEPARATOR_FUNCTION_PARTS, \
    COMMAND_SEPARATOR_ADDON, COMMAND_SEPARATOR_GROUP, CORE_COMMAND_NAME
from src.core.command.AbstractCommandProcessor import AbstractCommandProcessor


class AddonCommandProcessor(AbstractCommandProcessor):

    def get_pattern(self) -> str:
        return COMMAND_PATTERN_ADDON

    def get_type(self) -> str:
        return COMMAND_TYPE_ADDON

    def get_path(self, subdir: str = None) -> str | None:
        # Unable to find command path if no addon name found.
        if self.match.group(1) is None:
            return None

        return self.build_command_path(
            f"{self.kernel.path['addons']}{self.match.group(1)}/",
            subdir,
            os.path.join(self.match.group(2), self.match.group(3))
        )

    def get_function_name(self):
        return COMMAND_SEPARATOR_FUNCTION_PARTS.join([
            self.match.group(1),
            self.match.group(2),
            self.match.group(3),
        ])

    def build_command_parts(self, function_name):
        return function_name.split(COMMAND_SEPARATOR_FUNCTION_PARTS)[:3]

    def build_command_from_function(self, function) -> str | None:
        # Check if parent class returns something
        output = super().build_command_from_function(function)
        if output is not None:
            return output

        parts = self.build_command_parts(function.callback.__name__)

        return f'{parts[0]}{COMMAND_SEPARATOR_ADDON}{parts[1]}{COMMAND_SEPARATOR_GROUP}{parts[2]}'

    def build_full_command_from_function(self, function, args: dict = {}) -> str | None:
        # Check if parent class returns something
        output = super().build_full_command_from_function(function, args)
        if output is not None:
            return output

        output = f'{CORE_COMMAND_NAME} '
        output += self.build_command_from_function(function)

        if len(args):
            output += ' '.join(convert_dict_to_args(function, args))

        return output

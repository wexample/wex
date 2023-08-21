import os

from src.const.globals import COMMAND_PATTERN_ADDON, COMMAND_TYPE_ADDON, COMMAND_SEPARATOR_FUNCTION_PARTS
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

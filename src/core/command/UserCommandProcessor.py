import os
import sys

from src.const.globals import COMMAND_PATTERN_USER, COMMAND_TYPE_USER, COMMAND_SEPARATOR_FUNCTION_PARTS
from src.helper.user import get_user_home_data_path
from src.core.command.AbstractCommandProcessor import AbstractCommandProcessor


class UserCommandProcessor(AbstractCommandProcessor):
    def exec(self) -> str | None:
        # Add user command dir to path
        # It allows to use imports in custom user scripts
        user_data_path = get_user_home_data_path()
        commands_path = os.path.join(user_data_path, 'command')
        if os.path.exists(commands_path) and commands_path not in sys.path:
            sys.path.append(commands_path)

        return super().exec()

    def get_pattern(self) -> str:
        return COMMAND_PATTERN_USER

    def get_type(self) -> str:
        return COMMAND_TYPE_USER

    def get_path(self, subdir: str = None):
        return self.build_command_path(
            get_user_home_data_path(),
            subdir,
            os.path.join(self.match[2], self.match[3])
        )

    def get_function_name(self):
        return COMMAND_SEPARATOR_FUNCTION_PARTS.join([
            'user',
            self.match.group(2),
            self.match.group(3)
        ])

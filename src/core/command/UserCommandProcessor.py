import os
import sys

from addons.app.const.app import APP_DIR_APP_DATA
from src.helper.string import to_snake_case
from src.helper.system import get_user_or_sudo_user_home_data_path
from src.const.globals import COMMAND_PATTERN_USER, COMMAND_TYPE_USER, \
    COMMAND_CHAR_USER
from src.core.command.AbstractCommandProcessor import AbstractCommandProcessor


class UserCommandProcessor(AbstractCommandProcessor):
    def exec(self, quiet: bool = False) -> str | None:
        # Add user command dir to path
        # It allows to use imports in custom user scripts
        commands_path = os.path.join(self.get_base_path(), 'command')
        if os.path.exists(commands_path) and commands_path not in sys.path:
            sys.path.append(commands_path)

        return super().exec(quiet)

    def get_pattern(self) -> str:
        return COMMAND_PATTERN_USER

    def get_type(self) -> str:
        return COMMAND_TYPE_USER

    def get_path(self, subdir: str = None):
        return self.build_command_path(
            self.get_base_path(),
            subdir,
            os.path.join(to_snake_case(self.match[2]), to_snake_case(self.match[3]))
        )

    def get_base_path(self):
        return f'{get_user_or_sudo_user_home_data_path()}{APP_DIR_APP_DATA}'

    def get_function_name_parts(self) -> []:
        return [
            'user',
            self.match.group(2),
            self.match.group(3)
        ]

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        if cursor == 0:
            base_command_path = self.get_base_command_path()

            if os.path.exists(base_command_path):
                # User typed "~"
                if search_split[0].startswith(COMMAND_CHAR_USER):
                    from src.helper.suggest import suggest_from_path

                    return ' '.join(suggest_from_path(
                        base_command_path,
                        search_split[0],
                        COMMAND_CHAR_USER
                    ))
                # Cursor is at the beginning, suggest ~ char
                elif search_split[0] == '':
                    # Wrap to avoid resolution
                    return f'\\{COMMAND_CHAR_USER}'

        # Arguments
        elif cursor >= 1:
            if search_split[0].startswith(COMMAND_CHAR_USER):
                return self.suggest_arguments(
                    search_split[0],
                    search_split[1:],
                )
        return None

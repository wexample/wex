import os
import sys

from addons.app.const.app import APP_DIR_APP_DATA
from src.helper.system import get_user_or_sudo_user_home_data_path
from src.const.globals import COMMAND_PATTERN_USER, COMMAND_TYPE_USER, COMMAND_SEPARATOR_FUNCTION_PARTS, \
    COMMAND_CHAR_USER
from src.core.command.AbstractCommandProcessor import AbstractCommandProcessor


class UserCommandProcessor(AbstractCommandProcessor):
    def exec(self) -> str | None:
        # Add user command dir to path
        # It allows to use imports in custom user scripts
        user_data_path = f'{get_user_or_sudo_user_home_data_path()}{APP_DIR_APP_DATA}'
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
            f'{get_user_or_sudo_user_home_data_path()}{APP_DIR_APP_DATA}',
            subdir,
            os.path.join(self.match[2], self.match[3])
        )

    def get_function_name(self):
        return COMMAND_SEPARATOR_FUNCTION_PARTS.join([
            'user',
            self.match.group(2),
            self.match.group(3)
        ])

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        if cursor == 0:
            # User typed "~"
            if search_split[0].startswith(COMMAND_CHAR_USER):
                import os
                from src.helper.suggest import suggest_from_path

                return ' '.join(suggest_from_path(
                    f'{get_user_or_sudo_user_home_data_path()}{APP_DIR_APP_DATA}command/',
                    search_split[0],
                    COMMAND_CHAR_USER
                ))
            # Cursor is at the beginning, suggest ~ char
            elif search_split[0] == '':
                import os
                # User local command path exists
                base_path = f'{get_user_or_sudo_user_home_data_path()}{APP_DIR_APP_DATA}command/'

                if os.path.exists(base_path):
                    # Wrap to avoid resolution
                    return f'\\{COMMAND_CHAR_USER}'

        return None

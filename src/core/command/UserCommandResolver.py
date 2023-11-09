import os
import sys

from addons.app.const.app import APP_DIR_APP_DATA
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.helper.string import to_snake_case, to_kebab_case
from src.helper.system import get_user_or_sudo_user_home_data_path
from src.const.globals import COMMAND_PATTERN_USER, COMMAND_TYPE_USER, \
    COMMAND_CHAR_USER, COMMAND_SEPARATOR_GROUP
from src.core.command.AbstractCommandResolver import AbstractCommandResolver


class UserCommandResolver(AbstractCommandResolver):
    def render_request(self, request: CommandRequest, render_mode: str) -> AbstractResponse:
        # Add user command dir to path
        # It allows to use imports in custom user scripts
        commands_path = os.path.join(self.get_base_path(), 'command')
        if os.path.exists(commands_path) and commands_path not in sys.path:
            sys.path.append(commands_path)

        return super().render_request(request, render_mode)

    @classmethod
    def get_pattern(cls) -> str:
        return COMMAND_PATTERN_USER

    @classmethod
    def get_type(cls) -> str:
        return COMMAND_TYPE_USER

    def build_path(self, request: CommandRequest, extension: str, subdir: str = None) -> str | None:
        return self.build_command_path(
            base_path=self.get_base_path(),
            extension=extension,
            subdir=subdir,
            command_path=os.path.join(to_snake_case(request.match[2]), to_snake_case(request.match[3]))
        )

    def get_base_path(self):
        return f'{get_user_or_sudo_user_home_data_path()}{APP_DIR_APP_DATA}'

    def get_function_name_parts(self, parts: list) -> []:
        return [
            'user',
            parts[1],
            parts[2]
        ]

    def build_command_from_parts(self, parts: list) -> str:
        # Convert each part to kebab-case
        kebab_parts = [to_kebab_case(part) for part in parts]

        return f'{COMMAND_CHAR_USER}{kebab_parts[1]}{COMMAND_SEPARATOR_GROUP}{kebab_parts[2]}'

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        if cursor == 0:
            base_command_path = self.get_base_command_path()

            if os.path.exists(base_command_path):
                # User typed "~"
                if search_split[0].startswith(COMMAND_CHAR_USER):
                    return ' '.join(self.suggest_from_path(
                        base_command_path,
                        search_split[0],
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

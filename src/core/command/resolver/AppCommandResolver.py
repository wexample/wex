import os
from addons.app.const.app import APP_DIR_APP_DATA, ERR_APP_NOT_FOUND
from src.core.CommandRequest import CommandRequest
from src.core.response.AbortResponse import AbortResponse
from src.core.response.AbstractResponse import AbstractResponse
from src.helper.string import to_snake_case, to_kebab_case
from src.const.globals import COMMAND_PATTERN_APP, COMMAND_TYPE_APP, COMMAND_CHAR_APP, \
    COMMAND_SEPARATOR_GROUP
from src.core.command.resolver.AbstractCommandResolver import AbstractCommandResolver


class AppCommandResolver(AbstractCommandResolver):
    def __init__(self, kernel):
        super().__init__(kernel)

        # Shortcut.
        self.app_addon_manager = kernel.addons['app']

    def render_request(self, request: CommandRequest, render_mode: str) -> AbstractResponse:
        if not self.get_base_path():
            if not request.quiet:
                self.kernel.io.error(ERR_APP_NOT_FOUND, {
                    'command': request.command,
                    'dir': os.getcwd(),
                })

            return AbortResponse(self.kernel, reason=ERR_APP_NOT_FOUND)

        return super().render_request(request, render_mode)

    @classmethod
    def get_pattern(cls) -> str:
        return COMMAND_PATTERN_APP

    @classmethod
    def get_type(cls) -> str:
        return COMMAND_TYPE_APP

    def build_path(self, request: CommandRequest, extension: str, subdir: str = None) -> str | None:
        return self.build_command_path(
            base_path=self.get_base_path(),
            extension=extension,
            subdir=subdir,
            command_path=os.path.join(to_snake_case(request.match[2]), to_snake_case(request.match[3]))
        )

    def build_command_from_parts(self, parts: list) -> str:
        # Convert each part to kebab-case
        kebab_parts = [to_kebab_case(part) for part in parts]

        return f'{COMMAND_CHAR_APP}{kebab_parts[1]}{COMMAND_SEPARATOR_GROUP}{kebab_parts[2]}'

    def get_function_name_parts(self, parts: list) -> []:
        return [
            'app',
            parts[1],
            parts[2]
        ]

    def get_base_path(self):
        app_dir = self.app_addon_manager.app_dir
        if not self.app_addon_manager.app_dir:
            from addons.app.command.location.find import app__location__find

            app_dir = self.kernel.run_function(
                app__location__find,
                {
                    'app-dir': self.kernel.get_path('call')
                }
            ).first()

        if app_dir:
            return f'{app_dir}{APP_DIR_APP_DATA}'

        return None

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        if cursor == 0:
            # User typed "."
            if search_split[0].startswith(COMMAND_CHAR_APP):
                app_path = self.get_base_command_path()

                # We are in an app dir or subdir
                if app_path:
                    return ' '.join(
                        self.suggest_from_path(
                            app_path,
                            search_split[0],
                        )
                    )

            elif search_split[0] == '':
                # We are in an app dir or subdir
                if self.get_base_command_path():
                    # Suggest to execute local app command
                    return COMMAND_CHAR_APP

        # Arguments
        elif cursor >= 1:
            if search_split[0].startswith(COMMAND_CHAR_APP):
                return self.suggest_arguments(
                    search_split[0],
                    search_split[1:],
                )

        return None
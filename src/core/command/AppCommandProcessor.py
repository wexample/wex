import os

from addons.app.const.app import APP_DIR_APP_DATA, ERR_APP_NOT_FOUND
from src.const.globals import COMMAND_PATTERN_APP, COMMAND_TYPE_APP, COMMAND_SEPARATOR_FUNCTION_PARTS, COMMAND_CHAR_APP
from src.core.command.AbstractCommandProcessor import AbstractCommandProcessor


class AppCommandProcessor(AbstractCommandProcessor):
    def exec(self) -> str | None:
        if not self.kernel.addons['app']['path']['call_app_dir']:
            self.kernel.error(ERR_APP_NOT_FOUND, {
                'command': self.command,
                'dir': os.getcwd(),
            })

            return None

        return super().exec()

    def get_pattern(self) -> str:
        return COMMAND_PATTERN_APP

    def get_type(self) -> str:
        return COMMAND_TYPE_APP

    def get_path(self, subdir: str = None) -> str | None:
        return self.build_command_path(
            f"{self.kernel.addons['app']['path']['call_app_dir']}{APP_DIR_APP_DATA}",
            subdir,
            os.path.join(self.match[2], self.match[3])
        )

    def get_function_name(self):
        return COMMAND_SEPARATOR_FUNCTION_PARTS.join([
            'app',
            self.match.group(2),
            self.match.group(3)
        ])

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        if cursor == 0:
            # User typed "."
            if search_split[0].startswith(COMMAND_CHAR_APP):
                from addons.app.command.location.find import app__location__find
                from src.helper.suggest import suggest_from_path

                app_path = self.kernel.exec_function(app__location__find)
                # We are in an app dir or subdir
                if app_path:
                    return ' '.join(
                        suggest_from_path(
                            f'{app_path}{APP_DIR_APP_DATA}command/',
                            search_split[0],
                            COMMAND_CHAR_APP
                        )
                    )

            elif search_split[0] == '':
                from addons.app.command.location.find import app__location__find
                # # We are in an app dir or subdir
                if self.kernel.exec_function(app__location__find):
                    # Suggest to execute local app command
                    return COMMAND_CHAR_APP

        return None

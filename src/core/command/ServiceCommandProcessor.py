from addons.app.const.app import ERR_SERVICE_NOT_FOUND
from src.const.globals import COMMAND_PATTERN_SERVICE, COMMAND_TYPE_SERVICE, COMMAND_SEPARATOR_FUNCTION_PARTS, \
    COMMAND_CHAR_SERVICE
from src.core.command.AbstractCommandProcessor import AbstractCommandProcessor


class ServiceCommandProcessor(AbstractCommandProcessor):
    def exec(self) -> str | None:
        if self.match[2] not in self.kernel.registry['services']:
            self.kernel.error(ERR_SERVICE_NOT_FOUND, {
                'command': self.command,
                'service': self.match[2],
            })
            return

        return super().exec()

    def get_pattern(self) -> str:
        return COMMAND_PATTERN_SERVICE

    def get_type(self) -> str:
        return COMMAND_TYPE_SERVICE

    def get_path(self, subdir: str = None):
        return self.build_command_path(
            f"{self.kernel.registry['services'][self.match[2]]['dir']}",
            subdir,
            self.match[3]
        )

    def get_function_name(self):
        return COMMAND_SEPARATOR_FUNCTION_PARTS.join([
            'service',
            self.match.group(2),
            self.match.group(3)
        ])

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        if cursor == 0:
            if search_split[0] == COMMAND_CHAR_SERVICE:
                from src.helper.registry import get_all_commands_from_services

                commands = [command for command in get_all_commands_from_services(self.kernel).keys() if command.startswith(search_split[0])]

                return ' '.join(commands)
            elif search_split[0] == '':
                return COMMAND_CHAR_SERVICE
        elif cursor == 1:
            # User typed "wex @x" so we can suggest service names.
            if search_split[0] == COMMAND_CHAR_SERVICE:
                from src.helper.registry import get_all_commands_from_services

                commands = [command for command in get_all_commands_from_services(self.kernel).keys() if command.startswith(search_split[0])]

                return ' '.join(commands)
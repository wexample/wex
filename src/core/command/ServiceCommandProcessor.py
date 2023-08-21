from addons.app.const.app import ERR_SERVICE_NOT_FOUND
from src.const.globals import COMMAND_PATTERN_SERVICE, COMMAND_TYPE_SERVICE, COMMAND_SEPARATOR_FUNCTION_PARTS
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

from addons.app.const.app import ERR_CORE_ACTION_NOT_FOUND
from src.const.globals import COMMAND_PATTERN_CORE, COMMAND_TYPE_CORE
from src.core.command.AbstractCommandProcessor import AbstractCommandProcessor


class CoreCommandProcessor(AbstractCommandProcessor):
    def exec(self) -> str | None:
        core_actions = self.kernel.get_core_actions()

        # Handle core action : test, hi, etc...
        if self.command in core_actions:
            action = self.command
            command = None
            if self.command_args:
                command = self.command_args.pop(0)

            action = core_actions[action](self.kernel)

            return action.exec(command, self.command_args)
        else:
            self.kernel.error(ERR_CORE_ACTION_NOT_FOUND, {
                'command': self.command,
            })
            return

    def get_pattern(self) -> str:
        return COMMAND_PATTERN_CORE

    def get_type(self) -> str:
        return COMMAND_TYPE_CORE

    def get_path(self, subdir: str = None) -> str | None:
        return None

    def get_function_name(self):
        return None

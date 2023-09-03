from addons.app.const.app import ERR_CORE_ACTION_NOT_FOUND
from src.core.response.AbortResponse import AbortResponse
from src.core.response.DefaultResponse import DefaultResponse
from src.core.response.AbstractResponse import AbstractResponse
from src.const.globals import COMMAND_PATTERN_CORE, COMMAND_TYPE_CORE
from src.core.command.AbstractCommandProcessor import AbstractCommandProcessor


class CoreCommandProcessor(AbstractCommandProcessor):
    def run(self, quiet: bool = False) -> AbstractResponse:
        core_actions = self.kernel.core_actions

        # Handle core action : test, hi, etc...
        if self.command in core_actions:
            action = self.command
            command = None
            if self.command_args:
                command = self.command_args.pop(0)

            action = core_actions[action](self.kernel)

            return DefaultResponse(
                action.exec(command, self.command_args)
            )
        else:
            if not quiet:
                self.kernel.error(ERR_CORE_ACTION_NOT_FOUND, {
                    'command': self.command,
                })
            return AbortResponse()

    @classmethod
    def get_pattern(cls) -> str:
        return COMMAND_PATTERN_CORE

    @classmethod
    def get_type(cls) -> str:
        return COMMAND_TYPE_CORE

    # def get_path(self, subdir: str = None) -> str | None:
    #     return None
    #
    # def get_function_name(self) -> str | None:
    #     return None
    #
    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        if cursor == 0:
            # Adds also all core actions.
            return ' '.join([command for command in self.kernel.core_actions if command.startswith(search_split[0])])

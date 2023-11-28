from abc import abstractmethod
from typing import TYPE_CHECKING, Any

import click

from src.const.args import ARGS_HELP
from src.const.types import StringsList
from src.core.CommandRequest import CommandRequest, HasRequest
from src.core.KernelChild import KernelChild
from src.core.response.AbortResponse import AbortResponse

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class AbstractCommandRunner(KernelChild, HasRequest):
    def __init__(self, kernel: "Kernel") -> None:
        KernelChild.__init__(self, kernel)
        HasRequest.__init__(self)

        self._path: None | CommandRequest

    @abstractmethod
    def get_command_type(self):
        pass

    @abstractmethod
    def get_options_names(self) -> StringsList:
        pass

    @abstractmethod
    def run(self) -> Any:
        pass

    def run_click_function(self, script_command) -> Any:
        try:
            ctx = script_command.click_command.make_context(
                "", self.get_request().args.copy() or []
            )
        # Click explicitly asked to exit, for example when using --help.
        except click.exceptions.Exit:
            return AbortResponse(self.kernel, reason="INFO_COMMAND")
        except Exception as e:
            # Show error message
            self.kernel.io.error(
                "Error when creating context for command function {function} : {error}",
                {
                    "function": script_command.click_command.callback.__name__,
                    "error": str(e),
                },
                trace=False,
            )

        # Remove extra params which have been defined only
        # to be shown in help section, but are used outside function
        for arg in ARGS_HELP:
            if arg in ctx.params:
                del ctx.params[arg]

        # Defines kernel as mais class to provide with pass_obj option.
        ctx.obj = self.get_request().first_arg

        return script_command.run_command(self, script_command.click_command, ctx)

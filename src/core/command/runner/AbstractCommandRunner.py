from src.core.CommandRequest import CommandRequest
from abc import abstractmethod
from src.core.response.AbortResponse import AbortResponse
from src.const.error import ERR_COMMAND_CONTEXT
from src.const.args import ARGS_HELP
import click


class AbstractCommandRunner:
    def __init__(self, request: CommandRequest):
        self.request: CommandRequest = request

    @abstractmethod
    def get_command_type(self):
        pass

    @abstractmethod
    def get_params(self) -> list:
        pass

    @abstractmethod
    def get_attr(self, name: str, default=None) -> bool:
        pass

    @abstractmethod
    def has_attr(self, name: str) -> bool:
        pass

    @abstractmethod
    def run(self):
        kernel = self.request.resolver.kernel

        try:
            ctx = self.request.function.make_context('', self.request.args.copy() or [])
        # Click explicitly asked to exit, for example when using --help.
        except click.exceptions.Exit:
            return AbortResponse(kernel, reason='INFO_COMMAND')
        except Exception as e:
            # Show error message
            kernel.io.error(
                ERR_COMMAND_CONTEXT,
                {
                    'function': self.request.function.callback.__name__,
                    'error': str(e)
                }
            )

        # Remove extra params which have been defined only
        # to be shown in help section, but are used outside function
        for arg in ARGS_HELP:
            if arg in ctx.params:
                del ctx.params[arg]

        # Defines kernel as mais class to provide with pass_obj option.
        ctx.obj = kernel

        return self.request.function.invoke(ctx)

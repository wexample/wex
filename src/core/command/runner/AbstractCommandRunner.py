from src.core.CommandRequest import CommandRequest
from abc import abstractmethod
import click
from src.core.response.AbortResponse import AbortResponse
from src.const.args import ARGS_HELP


class AbstractCommandRunner:
    def __init__(self, kernel):
        self.kernel = kernel
        self.request: None | CommandRequest = None

    def set_request(self, request: CommandRequest):
        self.request = request
        self.request.runner = self

    @abstractmethod
    def get_command_type(self):
        pass

    @abstractmethod
    def get_params(self) -> list:
        pass

    @abstractmethod
    def run(self):
        pass

    def run_click_function(self, click_function):
        try:
            ctx = click_function.make_context('', self.request.args.copy() or [])
        # Click explicitly asked to exit, for example when using --help.
        except click.exceptions.Exit:
            return AbortResponse(self.kernel, reason='INFO_COMMAND')
        except Exception as e:
            # Show error message
            self.kernel.io.error(
                "Error when creating context for command function {function} : {error}",
                {
                    'function': click_function.callback.__name__,
                    'error': str(e)
                }, trace=False
            )

        # Remove extra params which have been defined only
        # to be shown in help section, but are used outside function
        for arg in ARGS_HELP:
            if arg in ctx.params:
                del ctx.params[arg]

        # Defines kernel as mais class to provide with pass_obj option.
        ctx.obj = self.kernel

        return click_function.invoke(ctx)

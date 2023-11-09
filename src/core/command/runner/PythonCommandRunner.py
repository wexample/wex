import click

from click import Command
from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner
from src.helper.args import convert_dict_to_args
from src.core.CommandRequest import CommandRequest
from src.core.response.AbortResponse import AbortResponse
from src.const.error import ERR_COMMAND_CONTEXT
from src.const.args import ARGS_HELP


class PythonCommandRunner(AbstractCommandRunner):
    def __init__(self, kernel):
        super().__init__(kernel)

        self.function: None | Command = None

    def set_request(self, request: CommandRequest):
        super().set_request(request=request)

        self.function: Command = self.get_request_function(
            request.path,
            list(request.match.groups()))

    def convert_args_dict_to_list(self, args: dict) -> list:
        return convert_dict_to_args(self.function, args)

    def get_request_function(self, path: str, parts) -> Command:
        return self.request.resolver.get_function(
            path,
            parts
        )

    def get_params(self) -> list:
        return self.function.params

    def get_command_type(self):
        return self.function.callback.command_type

    def get_attr(self, name: str, default=None) -> bool:
        return getattr(self.function.callback, name, default)

    def has_attr(self, name: str) -> bool:
        return hasattr(self.function.callback, name)

    def run(self):
        kernel = self.request.resolver.kernel

        try:
            ctx = self.function.make_context('', self.request.args.copy() or [])
        # Click explicitly asked to exit, for example when using --help.
        except click.exceptions.Exit:
            return AbortResponse(kernel, reason='INFO_COMMAND')
        except Exception as e:
            # Show error message
            kernel.io.error(
                ERR_COMMAND_CONTEXT,
                {
                    'function': self.function.callback.__name__,
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

        return self.function.invoke(ctx)

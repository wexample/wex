from click import Command
from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner
from src.helper.args import convert_dict_to_args
from src.core.CommandRequest import CommandRequest


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
        return self.run_click_function(
            self.function
        )


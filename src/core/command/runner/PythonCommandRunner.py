from click import Command
from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner
from src.helper.args import args_convert_dict_to_args
from src.core.CommandRequest import CommandRequest


class PythonCommandRunner(AbstractCommandRunner):
    def set_request(self, request: CommandRequest):
        super().set_request(request=request)

    def convert_args_dict_to_list(self, args: dict) -> list:
        return args_convert_dict_to_args(self.request.function, args)

    def build_request_function(self) -> Command:
        return self.request.resolver.get_function(
            self.request.path,
            list(self.request.match.groups())
        )

    def get_params(self) -> list:
        return self.request.function.params

    def get_command_type(self):
        return self.request.function.callback.command_type

    def get_attr(self, name: str, default=None) -> bool:
        return getattr(self.request.function.callback, name, default)

    def has_attr(self, name: str) -> bool:
        return hasattr(self.request.function.callback, name)

    def run(self):
        return self.run_click_function(
            self.request.function
        )


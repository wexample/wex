import importlib.util
from typing import Any

from click import Command

from src.const.types import StringsList
from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner
from src.core.CommandRequest import CommandRequest


class PythonCommandRunner(AbstractCommandRunner):
    def set_request(self, request: CommandRequest):
        super().set_request(request=request)

    def build_script_command(self) -> Command:
        # Import module and load function.
        spec = importlib.util.spec_from_file_location(
            self.request.path, self.request.path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return getattr(
            module,
            self.request.resolver.get_function_name(list(self.request.match.groups())),
        )

    def get_options_names(self) -> StringsList:
        params: StringsList = []
        for param in self.request.script_command.function.params:
            params += param.opts

        return params

    def get_command_type(self) -> str:
        return self.request.script_command.function.callback.command_type

    def run(self) -> Any:
        return self.run_click_function(self.request.script_command)

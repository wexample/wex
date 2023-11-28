import importlib.util
from typing import Any, Optional, cast

from src.const.types import StringsList
from src.core.command.resolver.AbstractCommandResolver import AbstractCommandResolver
from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner
from src.core.command.ScriptCommand import ScriptCommand
from src.core.CommandRequest import CommandRequest


class PythonCommandRunner(AbstractCommandRunner):
    def set_request(self, request: CommandRequest) -> None:
        super().set_request(request=request)

    def build_script_command(self) -> Optional[ScriptCommand]:
        request = self.get_request()
        path = request.get_path()

        # Import module and load function.
        spec = importlib.util.spec_from_file_location(path, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        resolver = cast(AbstractCommandResolver, request.resolver)

        return getattr(
            module,
            resolver.get_function_name(list(request.get_match().groups())),
        )

    def get_options_names(self) -> StringsList:
        params: StringsList = []
        for param in self.get_request().get_script_command().click_command.params:
            params += param.opts

        return params

    def get_command_type(self) -> str:
        return self.get_request().get_script_command().command_type

    def run(self) -> Any:
        return self.run_click_function(self.get_request().get_script_command())

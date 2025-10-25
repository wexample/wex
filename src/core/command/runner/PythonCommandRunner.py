from __future__ import annotations
from typing import Any, cast

from src.const.types import StringsList
from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand


class PythonCommandRunner(AbstractCommandRunner):
    def build_script_command(self) -> ScriptCommand | None:
        from src.core.command.ScriptCommand import ScriptCommand
        from importlib import util
        request = self.get_request()
        path = request.get_path()

        # Import module and load function.
        spec = util.spec_from_file_location(path, path)

        if not spec or not spec.loader:
            return None

        module = util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return cast(
            ScriptCommand,
            getattr(
                module,
                request.resolver.get_function_name(list(request.get_match().groups())),
            ),
        )

    def get_command_type(self) -> str:
        return self.get_request().get_script_command().command_type

    def get_options_names(self) -> StringsList:
        params: StringsList = []
        for param in self.get_request().get_script_command().click_command.params:
            params += param.opts

        return params

    def run(self) -> Any:
        return self.run_click_function(self.get_request().get_script_command())

import importlib.util

from click import Command

from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner
from src.core.CommandRequest import CommandRequest


class PythonCommandRunner(AbstractCommandRunner):
    def set_request(self, request: CommandRequest):
        super().set_request(request=request)

    def build_script_command(self) -> Command:
        # Import module and load function.
        spec = importlib.util.spec_from_file_location(
            self.request.path,
            self.request.path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return getattr(
            module,
            self.request.resolver.get_function_name(
                list(self.request.match.groups())
            )
        )

    def get_params(self) -> list:
        return self.request.function.function.params

    def get_command_type(self):
        return self.request.function.function.callback.command_type

    def run(self):
        return self.run_click_function(
            self.request.function
        )


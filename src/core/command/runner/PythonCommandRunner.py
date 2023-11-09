from click import Command

from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner


class PythonCommandRunner(AbstractCommandRunner):
    def __init__(self, request):
        super().__init__(request)

        self.function: Command = self.get_request_function(
            request.path,
            list(request.match.groups()))

        # TODO Remove request.function ?
        request.function = self.function

    def get_request_function(self, path: str, parts) -> Command:
        return self.request.resolver.get_function(
            path,
            parts
        )

    def get_params(self) -> list:
        return self.request.function.params

    def get_command_type(self):
        return self.function.callback.command_type

    def get_attr(self, name: str, default=None) -> bool:
        return getattr(self.request.function.callback, name, default)

    def has_attr(self, name: str) -> bool:
        return hasattr(self.request.function.callback, name)

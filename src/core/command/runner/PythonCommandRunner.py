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

    def get_command_type(self):
        return self.function.callback.command_type

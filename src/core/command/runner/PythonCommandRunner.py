from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner


class PythonCommandRunner(AbstractCommandRunner):
    def __init__(self, request):
        super().__init__(request)

        request.function = self.get_request_function(
            request.path,
            list(request.match.groups()))

    def get_request_function(self, path: str, parts) -> str:
        return self.request.resolver.get_function(
            path,
            parts
        )

    def run(self):
        request = self.request
        kernel = self.request.resolver.kernel



from src.core.CommandRequest import CommandRequest


class AbstractCommandRunner:
    def __init__(self, request: CommandRequest):
        self.request: CommandRequest = request

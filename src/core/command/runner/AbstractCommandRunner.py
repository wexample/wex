from src.core.CommandRequest import CommandRequest
from abc import abstractmethod


class AbstractCommandRunner:
    def __init__(self, request: CommandRequest):
        self.request: CommandRequest = request

    @abstractmethod
    def get_command_type(self):
        pass
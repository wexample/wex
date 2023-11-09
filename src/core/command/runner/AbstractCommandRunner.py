from src.core.CommandRequest import CommandRequest
from abc import abstractmethod


class AbstractCommandRunner:
    def __init__(self, request: CommandRequest):
        self.request: CommandRequest = request

    @abstractmethod
    def run(self):
        pass
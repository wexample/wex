from src.core.CommandRequest import CommandRequest
from abc import abstractmethod


class AbstractCommandRunner:
    def __init__(self, request: CommandRequest):
        self.request: CommandRequest = request

    @abstractmethod
    def get_command_type(self):
        pass

    @abstractmethod
    def get_params(self) -> list:
        pass

    @abstractmethod
    def get_attr(self, name: str, default=None) -> bool:
        pass

    @abstractmethod
    def has_attr(self, name: str) -> bool:
        pass

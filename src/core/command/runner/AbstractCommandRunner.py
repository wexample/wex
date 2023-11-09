from src.core.CommandRequest import CommandRequest
from abc import abstractmethod


class AbstractCommandRunner:
    def __init__(self, kernel):
        self.kernel = kernel
        self.request: None | CommandRequest = None

    def set_request(self, request: CommandRequest):
        self.request = request
        self.request.runner = self

    @abstractmethod
    def convert_args_dict_to_list(self, args: dict) -> list:
        pass

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

    @abstractmethod
    def run(self):
        pass

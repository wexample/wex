from abc import abstractmethod


class AbstractCoreAction:
    kernel = None

    def __init__(self, kernel):
        self.kernel = kernel

    @abstractmethod
    def exec(self, command, command_args):
        pass

    @staticmethod
    @abstractmethod
    def command() -> str:
        pass

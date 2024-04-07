from abc import abstractmethod

from src.core.KernelChild import KernelChild


class AbstractChatSubject(KernelChild):
    @abstractmethod
    def name(self) -> str:
        pass

    def introduce(self) -> str:
        return self.name()

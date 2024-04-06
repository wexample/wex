from abc import abstractmethod

from src.core.KernelChild import KernelChild


class AbstractChatSubject(KernelChild):
    @abstractmethod
    def name(self) -> str:
        pass

from abc import abstractmethod
from typing import TYPE_CHECKING, Optional

from src.core.KernelChild import KernelChild

if TYPE_CHECKING:
    from langchain_core.language_models import BaseLLM

    from src.core.Kernel import Kernel


class AbstractModel(KernelChild):
    llm: Optional["BaseLLM"]

    def __init__(self, kernel: "Kernel", name: str):
        super().__init__(kernel)

        self.name: str = name

    @abstractmethod
    def activate(self):
        pass

from abc import abstractmethod
from typing import TYPE_CHECKING, Optional

from src.const.types import StringKeysDict
from src.core.KernelChild import KernelChild

if TYPE_CHECKING:
    from langchain_core.language_models import BaseLLM

    from src.core.Kernel import Kernel


class AbstractModel(KernelChild):
    llm: Optional["BaseLLM"]

    def __init__(self, kernel: "Kernel", identifier: str):
        super().__init__(kernel)

        self.identifier = identifier
        service, name = identifier.split(':')

        self.service: str = service
        self.name: str = name

    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def request(
        self,
        input: str,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict):
        pass

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Optional, List
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseLanguageModel
from src.const.types import StringKeysDict
from src.core.KernelChild import KernelChild
from src.helper.dict import dict_merge

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class AbstractModel(KernelChild):
    _llm: Optional[BaseLanguageModel[Any]]

    def set_llm(self, llm: BaseLanguageModel[Any]) -> None:
        self._llm = llm

    def get_llm(self) -> BaseLanguageModel[Any]:
        self._validate__should_not_be_none(self._llm)
        assert isinstance(self._llm, BaseLanguageModel)

        return self._llm

    def __init__(self, kernel: "Kernel", identifier: str):
        super().__init__(kernel)

        self.identifier = identifier
        service, name = identifier.split(":")

        self.service: str = service
        self.name: str = name
        self.activate()

    def chat_create_prompt(self, identity: StringKeysDict) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", identity["system"]),
                ("human", "{input}"),
            ]
        )

    def chat_merge_parameters(
        self,
        input: str,
        identity_parameters: StringKeysDict
    ) -> StringKeysDict:
        return dict_merge({"input": input}, identity_parameters or {})

    @abstractmethod
    def choose_command(
        self,
        input: str,
        commands: List[str | None],
        instruction: str = "Return one command name, but only if could help answer user message, None instead"
    ) -> Optional[str]:
        return None

    @abstractmethod
    def activate(self) -> None:
        pass

    @abstractmethod
    def request(
        self,
        input: str,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict
    ) -> Any:
        pass

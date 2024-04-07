from abc import abstractmethod
from typing import TYPE_CHECKING, Any, List, Optional, Union, cast

from langchain.agents import BaseMultiActionAgent, BaseSingleActionAgent
from langchain.chains.llm import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseLanguageModel

from addons.ai.src.tool.command_tool import CommandTool
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

    def __init__(self, kernel: "Kernel", identifier: str) -> None:
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
        self, input: str, identity_parameters: StringKeysDict
    ) -> StringKeysDict:
        return dict_merge({"input": input}, identity_parameters or {})

    def create_embeddings(self) -> Any:
        return None

    def chat(
        self, input: str, identity: StringKeysDict, identity_parameters: StringKeysDict
    ) -> Any:
        chain = LLMChain(
            llm=self.get_llm(), prompt=self.chat_create_prompt(identity), verbose=False
        )

        return chain.invoke(self.chat_merge_parameters(input, identity_parameters))[
            "text"
        ].strip()

    def chat_agent(
        self, question: str, tools: List[CommandTool], identity: StringKeysDict
    ) -> str:
        from langchain.agents import AgentExecutor, create_react_agent

        prompt = self.chat_create_prompt(identity)

        agent = cast(
            Union[BaseSingleActionAgent, BaseMultiActionAgent],
            create_react_agent(self.get_llm(), tools, prompt=prompt),
        )

        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        return str(agent_executor.invoke({"input": question})["output"])

    @abstractmethod
    def choose_command(
        self,
        input: str,
        commands: List[str | None],
        identity: StringKeysDict,
    ) -> Optional[str]:
        return None

    @abstractmethod
    def activate(self) -> None:
        pass

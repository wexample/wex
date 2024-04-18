from abc import abstractmethod
from typing import TYPE_CHECKING, Any, List, Optional, Union, cast

from langchain.agents import BaseMultiActionAgent, BaseSingleActionAgent
from langchain.chains.llm import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import BasePromptTemplate
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

from addons.ai.src.assistant.utils.abstract_assistant_child import AbstractAssistantChild
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from addons.ai.src.tool.command_tool import CommandTool
from src.const.types import StringKeysDict, StringsList
from src.helper.dict import dict_merge

if TYPE_CHECKING:
    from addons.ai.src.assistant.assistant import Assistant


class AbstractModel(AbstractAssistantChild):
    _llm: Optional[BaseLanguageModel[Any]]

    def __init__(self, assistant: "Assistant", identifier: str) -> None:
        super().__init__(assistant)

        self.identifier = identifier
        service, name = identifier.split(":")

        self.service: str = service
        self.name: str = name
        self.activated: bool = False

    def set_llm(self, llm: BaseLanguageModel[Any]) -> None:
        self._llm = llm

    def get_llm(self) -> BaseLanguageModel[Any]:
        self._validate__should_not_be_none(self._llm)
        assert isinstance(self._llm, BaseLanguageModel)

        return self._llm

    def chat_create_prompt(self, user_prompt: UserPromptSection) -> ChatPromptTemplate:
        assistant = self.assistant

        return ChatPromptTemplate.from_messages(
            [
                ("system",
                 "##YOUR PERSONALITY\n" + (assistant.personalities[assistant.personality]["prompt"] or "")),
                ("system",
                 f"##LANGUAGE\nYou use \"{assistant.languages[assistant.language]}\" language in every text."),
                ("system",
                 "##INSTRUCTIONS\n" + assistant.get_current_subject().interaction_mode.get_initial_prompt()),
                ("human",
                 "{input}"),
            ]
        )

    def chat_merge_parameters(
        self, user_input: str, identity_parameters: StringKeysDict
    ) -> StringKeysDict:
        return dict_merge({"input": user_input}, identity_parameters or {})

    def create_embeddings(self) -> Any:
        return None

    def chat(
        self,
        prompt_section: UserPromptSection,
        identity_parameters: StringKeysDict,
    ) -> str:
        return self.chain_invoke_and_strip_result(
            prompt_template=self.chat_create_prompt(prompt_section),
            user_input=prompt_section.prompt,
            identity_parameters=identity_parameters,
        )

    def create_few_shot_prompt_template(
        self,
        identity: StringKeysDict,
        example_prompt: str,
        examples: List[StringKeysDict],
        input_variables_names: StringsList,
        response_variable_name: str = "response"
    ) -> FewShotPromptTemplate:
        example_prompt_template = PromptTemplate(
            input_variables=input_variables_names + [response_variable_name],
            template=example_prompt + "{" + response_variable_name + "}",
        )

        return FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt_template,
            # The prefix is our instructions
            prefix=identity["system"],
            # The suffix our user input and output indicator
            suffix=example_prompt,
            input_variables=input_variables_names,
            example_separator="\n----------------------------------\n",
        )

    def chat_with_few_shots(
        self,
        user_input,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict,
        example_prompt,
        examples,
        input_variables_names
    ):
        return self.chain_invoke_and_strip_result(
            prompt_template=self.create_few_shot_prompt_template(
                identity=identity,
                example_prompt=example_prompt,
                examples=examples,
                input_variables_names=input_variables_names
            ),
            user_input=user_input,
            identity_parameters=identity_parameters
        )

    def chat_agent(
        self, user_input: str, tools: List[CommandTool], identity: StringKeysDict
    ) -> str:
        from langchain.agents import AgentExecutor, create_react_agent

        prompt = self.chat_create_prompt(identity)

        agent = cast(
            Union[BaseSingleActionAgent, BaseMultiActionAgent],
            create_react_agent(self.get_llm(), tools, prompt=prompt),
        )

        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # @see https://github.com/langchain-ai/langchain/discussions/6598
        # At the moment there is a loop issue with agents
        return str(agent_executor.invoke({"input": user_input})["output"])

    def chain_invoke_and_strip_result(
        self,
        prompt_template: BasePromptTemplate,
        user_input: str,
        identity_parameters: StringKeysDict,
    ) -> str:
        chain = LLMChain(llm=self.get_llm(), prompt=prompt_template, verbose=False)

        return chain.invoke(
            self.chat_merge_parameters(user_input, identity_parameters)
        )["text"].strip()

    @abstractmethod
    def guess_function(
        self,
        user_input: str,
        functions: List[str | None],
        identity: StringKeysDict,
    ) -> Optional[str]:
        return None

    @abstractmethod
    def activate(self) -> None:
        self.activated = True

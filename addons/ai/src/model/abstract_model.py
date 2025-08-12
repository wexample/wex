from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union, cast

from langchain.agents import BaseMultiActionAgent, BaseSingleActionAgent
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts import (
    BasePromptTemplate,
    FewShotPromptTemplate,
    PromptTemplate,
)
from langchain_core.runnables import ConfigurableFieldSpec, Runnable
from langchain_core.runnables.history import RunnableWithMessageHistory
from wexample_helpers.helpers.dict import dict_merge

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import (
    AbstractInteractionMode,
)
from addons.ai.src.assistant.utils.abstract_assistant_child import (
    AbstractAssistantChild,
)
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from addons.ai.src.tool.command_tool import CommandTool
from src.const.types import StringKeysDict, StringsList

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

    def chat_create_prompt(
        self,
        interaction_mode: AbstractInteractionMode,
        prompt_section: UserPromptSection,
    ) -> ChatPromptTemplate:
        assistant = self.assistant

        parts: List[tuple[str, str]] = []
        personalities = cast(Dict[str, Dict[str, Any]], assistant.personalities)
        personality_conf = personalities.get(assistant.personality, {})
        raw_personality_prompt = personality_conf.get("prompt")
        personality_prompt = (
            str(raw_personality_prompt) if raw_personality_prompt is not None else ""
        )
        if personality_prompt:
            parts.append(
                ("system", "##YOUR PERSONALITY\n" + personality_prompt),
            )

        parts += [
            (
                "system",
                f"##LANGUAGE"
                f'\nYou use "{str(cast(Dict[str, Any], assistant.languages).get(assistant.language, ""))}" language in every text, '
                f"even if the person uses another language, unless you are explicitly asked to do otherwise.",
            ),
        ]

        initial_prompt = interaction_mode.get_initial_prompt(prompt_section) or ""
        if initial_prompt:
            parts += [
                ("system", "##INSTRUCTIONS\n" + initial_prompt),
            ]

        if len(self.assistant.active_memory.messages):
            parts += [
                ("system", "##CONVERSATION HISTORY\n{history}"),
            ]

        parser = interaction_mode.get_output_parser(prompt_section)
        if parser:
            parts += [
                ("system", "{format_instructions}"),
            ]

        return ChatPromptTemplate.from_messages(
            parts + prompt_section.prompt_configurations + [("human", "{input}")]
        )

    def create_embeddings(self) -> Any:
        return None

    def chat(
        self,
        interaction_mode: AbstractInteractionMode,
        prompt_section: UserPromptSection,
        prompt_parameters: Optional[StringKeysDict] = None,
    ) -> str:
        return self.chain_invoke_and_parse(
            interaction_mode=interaction_mode,
            prompt_template=self.chat_create_prompt(interaction_mode, prompt_section),
            prompt_section=prompt_section,
            prompt_parameters=prompt_parameters,
        )

    def create_few_shot_prompt_template(
        self,
        interaction_mode: Optional[AbstractInteractionMode] = None,
        prompt_section: Optional[UserPromptSection] = None,
        example_prompt: str = "",
        examples: List[StringKeysDict] = [],
        input_variables_names: StringsList = [],
        response_variable_name: str = "response",
    ) -> FewShotPromptTemplate:
        example_prompt_template = PromptTemplate(
            input_variables=input_variables_names + [response_variable_name],
            template=example_prompt + "{" + response_variable_name + "}",
        )

        # Determine prefix from interaction mode if provided
        prefix_text = (
            interaction_mode.get_initial_prompt(prompt_section)
            if interaction_mode and prompt_section
            else ""
        ) or ""

        return FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt_template,
            # The prefix is our instructions
            prefix=prefix_text,
            # The suffix our user input and output indicator
            suffix=example_prompt,
            input_variables=input_variables_names,
            example_separator="\n----------------------------------\n",
        )

    def chat_with_few_shots(
        self,
        interaction_mode: AbstractInteractionMode,
        prompt_section: UserPromptSection,
        prompt_parameters: StringKeysDict,
        example_prompt: str,
        examples: List[StringKeysDict],
        input_variables_names: StringsList,
    ) -> str:
        return self.chain_invoke_and_parse(
            interaction_mode=interaction_mode,
            prompt_template=self.create_few_shot_prompt_template(
                interaction_mode=interaction_mode,
                prompt_section=prompt_section,
                example_prompt=example_prompt,
                examples=examples,
                input_variables_names=input_variables_names,
            ),
            prompt_section=prompt_section,
            prompt_parameters=prompt_parameters,
        )

    def chat_agent(
        self,
        interaction_mode: AbstractInteractionMode,
        prompt_section: UserPromptSection,
        tools: List[CommandTool],
    ) -> str:
        from langchain.agents import AgentExecutor, create_react_agent

        prompt_template = self.chat_create_prompt(interaction_mode, prompt_section)

        agent = cast(
            Union[BaseSingleActionAgent, BaseMultiActionAgent],
            create_react_agent(self.get_llm(), tools, prompt=prompt_template),
        )

        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # @see https://github.com/langchain-ai/langchain/discussions/6598
        # At the moment there is a loop issue with agents
        return str(agent_executor.invoke({"input": prompt_section.prompt})["output"])

    def chain_invoke_and_parse(
        self,
        interaction_mode: AbstractInteractionMode,
        prompt_template: BasePromptTemplate[Any],
        prompt_section: UserPromptSection,
        prompt_parameters: Optional[StringKeysDict] = None,
    ) -> str:
        model = self.get_llm()
        chain_serializable = prompt_template | model
        chain = cast(Runnable[Dict[str, Any], Any], chain_serializable)

        with_message_history = RunnableWithMessageHistory(
            cast(
                Runnable[
                    Union[Sequence[BaseMessage], Dict[str, Any]],
                    Union[str, BaseMessage, Sequence[BaseMessage], Dict[str, Any]],
                ],
                chain,
            ),
            self.assistant.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
            history_factory_config=[
                ConfigurableFieldSpec(
                    id="user_id",
                    annotation=str,
                    name="User ID",
                    description="Unique identifier for the user.",
                    default="",
                    is_shared=True,
                ),
                ConfigurableFieldSpec(
                    id="conversation_id",
                    annotation=str,
                    name="Conversation ID",
                    description="Unique identifier for the conversation.",
                    default="",
                    is_shared=True,
                ),
            ],
        )

        parser = interaction_mode.get_output_parser(prompt_section)
        config: Dict[str, Dict[str, Any]] = {
            "configurable": {
                "user_id": self.assistant.user.id,
                "conversation_id": self.assistant.conversation.id,
            }
        }

        input_data = dict_merge(
            {"input": prompt_section.prompt},
            self.assistant.get_current_subject().get_prompt_parameters(),
            prompt_parameters or {},
        )

        if parser:
            input_data["format_instructions"] = parser.get_format_instructions()
            return interaction_mode.chain_response_to_string(
                prompt_section,
                (with_message_history | parser).invoke(input_data, cast(Any, config)),
            )
        else:
            return interaction_mode.chain_response_to_string(
                prompt_section,
                with_message_history.invoke(input_data, cast(Any, config)),
            )

    @abstractmethod
    def guess_function(
        self,
        interaction_mode: AbstractInteractionMode,
        prompt_section: UserPromptSection,
        functions: List[str | None],
    ) -> Optional[str]:
        return None

    @abstractmethod
    def activate(self) -> None:
        self.activated = True

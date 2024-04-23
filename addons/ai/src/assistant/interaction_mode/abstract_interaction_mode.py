from typing import Optional, List, TYPE_CHECKING, Dict, Any

from langchain_core.output_parsers import BaseOutputParser

from addons.ai.src.assistant.utils.abstract_assistant_child import AbstractAssistantChild
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection

if TYPE_CHECKING:
    from ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject


class AbstractInteractionMode(AbstractAssistantChild):
    def __init__(self, subject: "AbstractChatSubject"):
        super().__init__(subject.assistant)

        self._output_formatting_prompt: Optional[str] = None

    @staticmethod
    def name() -> str:
        pass

    def get_initial_prompt(self, prompt_section: UserPromptSection) -> Optional[str]:
        return None

    def get_interaction_mode_prompt_parameters(self, prompt_section: UserPromptSection) -> Dict[str, str]:
        return {}

    def set_output_formatting_prompt(self, prompt: str) -> None:
        if self._output_formatting_prompt is None:
            self._output_formatting_prompt = ''

        self._output_formatting_prompt += prompt

    def flush_output_formatting_prompt(self) -> Optional[str]:
        prompt = self._output_formatting_prompt
        self._output_formatting_prompt = None

        return prompt

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[bool | str]:
        self.assistant.spinner.start()

        response = self.assistant.get_model().chat(
            self,
            prompt_section,
            self.get_interaction_mode_prompt_parameters(prompt_section),
        )

        self.assistant.spinner.stop()

        return response

    def get_output_parser(self, prompt_section: UserPromptSection) -> Optional[BaseOutputParser]:
        return None

    def chain_response_to_string(
        self,
        prompt_section: UserPromptSection,
        chain_response: Any
    ) -> str:
        return chain_response.content

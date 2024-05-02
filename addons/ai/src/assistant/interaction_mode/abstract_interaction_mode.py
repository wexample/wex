from typing import TYPE_CHECKING, Any, Dict, List, Optional

from langchain_core.output_parsers import BaseOutputParser

from addons.ai.src.assistant.utils.abstract_assistant_child import (
    AbstractAssistantChild,
)
from addons.ai.src.assistant.interaction_response.string_interaction_response import StringInteractionResponse
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class AbstractInteractionMode(AbstractAssistantChild):
    @staticmethod
    def name() -> str:
        pass

    def get_initial_prompt(self, prompt_section: "UserPromptSection") -> Optional[str]:
        return None

    def get_interaction_mode_prompt_parameters(
        self, prompt_section: "UserPromptSection"
    ) -> Dict[str, str]:
        return {}

    def process_user_input(
        self,
        prompt_section: "UserPromptSection",
        remaining_sections: List["UserPromptSection"],
    ) -> AbstractInteractionResponse:
        self.assistant.spinner.start()

        response = self.assistant.get_model().chat(
            self,
            prompt_section,
            self.get_interaction_mode_prompt_parameters(prompt_section),
        )

        self.assistant.spinner.stop()

        return StringInteractionResponse(response)

    def get_output_parser(
        self, prompt_section: "UserPromptSection"
    ) -> Optional[BaseOutputParser]:
        return None

    def chain_response_to_string(
        self, prompt_section: "UserPromptSection", chain_response: Any
    ) -> str:
        return chain_response.content

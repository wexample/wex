from __future__ import annotations

from typing import TYPE_CHECKING, Any

from langchain_core.output_parsers import BaseOutputParser

from addons.ai.src.assistant.interaction_response.abstract_interaction_response import (
    AbstractInteractionResponse,
)
from addons.ai.src.assistant.interaction_response.string_interaction_response import (
    StringInteractionResponse,
)
from addons.ai.src.assistant.utils.abstract_assistant_child import (
    AbstractAssistantChild,
)

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class AbstractInteractionMode(AbstractAssistantChild):
    def chain_response_to_string(
        self, prompt_section: UserPromptSection, chain_response: Any
    ) -> str:
        return str(chain_response.content)

    def get_initial_prompt(self, prompt_section: UserPromptSection) -> str | None:
        return None

    def get_interaction_mode_prompt_parameters(
        self, prompt_section: UserPromptSection
    ) -> dict[str, str]:
        return {}

    def get_output_parser(
        self, prompt_section: UserPromptSection
    ) -> BaseOutputParser[Any] | None:
        return None

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: list[UserPromptSection],
    ) -> AbstractInteractionResponse:
        self.assistant.spinner.start()

        response = self.assistant.get_model().chat(
            self,
            prompt_section,
            self.get_interaction_mode_prompt_parameters(prompt_section),
        )

        self.assistant.spinner.stop()

        return StringInteractionResponse(response)

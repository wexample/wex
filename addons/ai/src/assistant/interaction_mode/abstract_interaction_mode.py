from typing import Optional, List, TYPE_CHECKING

from addons.ai.src.assistant.utils.abstract_assistant_child import AbstractAssistantChild
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection

if TYPE_CHECKING:
    from addons.ai.src.assistant.assistant import Assistant


class AbstractInteractionMode(AbstractAssistantChild):
    def __init__(self, assistant: "Assistant"):
        super().__init__(assistant)

        self._output_formatting_prompt: Optional[str] = None

    @staticmethod
    def name() -> str:
        pass

    def get_initial_prompt(self) -> Optional[str]:
        return None

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
        return None

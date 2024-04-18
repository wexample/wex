from typing import Optional, List

from addons.ai.src.assistant.assistant import Assistant
from addons.ai.src.assistant.utils.abstract_assistant_child import AbstractAssistantChild
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject


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
        subject: AbstractChatSubject,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[bool | str]:
        return None

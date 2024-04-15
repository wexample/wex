from typing import Optional, List

from addons.ai.src.assistant.utils.abstract_assistant_child import AbstractAssistantChild
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict


class AbstractChatSubject(AbstractAssistantChild):
    @staticmethod
    def name() -> str:
        pass

    def get_completer_commands(self) -> StringKeysDict:
        return {}

    def introduce(self) -> str:
        return self.name()

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[str]:
        return None

    def is_current_subject(self) -> bool:
        return self.assistant.get_current_subject() == self

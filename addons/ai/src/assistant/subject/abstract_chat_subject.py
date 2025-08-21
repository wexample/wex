from typing import Dict, Optional

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import \
    AbstractInteractionMode
from addons.ai.src.assistant.utils.abstract_assistant_child import \
    AbstractAssistantChild
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict


class AbstractChatSubject(AbstractAssistantChild):
    interaction_modes: Dict[str, AbstractInteractionMode]
    interaction_mode: Optional[AbstractInteractionMode]

    @staticmethod
    def name() -> str:
        return ""

    def activate(self, prompt_section: Optional[UserPromptSection] = None) -> bool:
        return True

    def get_commands(self) -> StringKeysDict:
        return {}

    def introduce(self) -> str:
        return self.name()

    def is_current_subject(self) -> bool:
        return self.assistant.get_current_subject() == self

    def get_prompt_parameters(self) -> Dict[str, str]:
        return {}

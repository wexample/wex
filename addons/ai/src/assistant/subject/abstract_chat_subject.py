from abc import abstractmethod
from typing import Dict, List, Optional

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import (
    AbstractInteractionMode,
)
from addons.ai.src.assistant.utils.abstract_assistant_child import (
    AbstractAssistantChild,
)
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict


class AbstractChatSubject(AbstractAssistantChild):
    interaction_modes: Dict[str, AbstractInteractionMode]
    interaction_mode: Optional[AbstractInteractionMode]

    @staticmethod
    def name() -> str:
        pass

    def get_commands(self) -> StringKeysDict:
        return {}

    def introduce(self) -> str:
        return self.name()

    @abstractmethod
    def get_interaction_mode(
        self, prompt_section: Optional[UserPromptSection] = None
    ) -> Optional[type]:
        pass

    def is_current_subject(self) -> bool:
        return self.assistant.get_current_subject() == self

    def get_prompt_parameters(self) -> Dict:
        return {}


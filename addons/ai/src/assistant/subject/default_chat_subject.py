from typing import List, Optional

from addons.ai.src.assistant.interaction_mode.default_interaction_mode import DefaultInteractionMode
from addons.ai.src.assistant.interaction_mode.investigation_interaction_mode import InvestigationInteractionMode
from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict

ASSISTANT_INTERACTION_MODE_DEFAULT = "default"
ASSISTANT_INTERACTION_MODE_INVESTIGATE = "investigate"


class DefaultChatSubject(AbstractChatSubject):
    @staticmethod
    def name() -> str:
        return "default"

    def get_interaction_modes(self) -> List[type]:
        return [
            DefaultInteractionMode,
            InvestigationInteractionMode
        ]

    def is_fallback_subject(self) -> bool:
        return True

    def get_completer_commands(self) -> StringKeysDict:
        commands = {
            ASSISTANT_INTERACTION_MODE_DEFAULT: "Free talk",
        }

        if self.is_current_subject():
            commands[ASSISTANT_INTERACTION_MODE_INVESTIGATE] = "Focus on fixing a problem"

        return commands

    def get_interaction_mode(self, prompt_section: Optional[UserPromptSection] = None) -> Optional[type]:
        if prompt_section and prompt_section.command == ASSISTANT_INTERACTION_MODE_INVESTIGATE:
            return InvestigationInteractionMode
        return DefaultInteractionMode

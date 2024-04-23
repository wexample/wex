from typing import List, Optional

from addons.ai.src.assistant.interaction_mode.default_interaction_mode import DefaultInteractionMode
from addons.ai.src.assistant.interaction_mode.formated_data_interaction_mode import FORMATED_DATA_FORMATS, \
    FormatedDataInteractionMode
from addons.ai.src.assistant.interaction_mode.investigation_interaction_mode import InvestigationInteractionMode
from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict

SUBJECT_DEFAULT_DEFAULT = "default"
SUBJECT_DEFAULT_INVESTIGATE = "investigate"
SUBJECT_DEFAULT_FORMAT = "format"


class DefaultChatSubject(AbstractChatSubject):
    @staticmethod
    def name() -> str:
        return "default"

    def get_interaction_modes(self) -> List[type]:
        return [
            DefaultInteractionMode,
            InvestigationInteractionMode,
            FormatedDataInteractionMode
        ]

    def is_fallback_subject(self) -> bool:
        return True

    def get_commands(self) -> StringKeysDict:
        commands = {
            SUBJECT_DEFAULT_DEFAULT: "Free talk",
            SUBJECT_DEFAULT_FORMAT: {
                "description": f"Return formated response",
                "options": FORMATED_DATA_FORMATS
            }
        }

        if self.is_current_subject():
            commands[SUBJECT_DEFAULT_INVESTIGATE] = "Focus on fixing a problem"

        return commands

    def get_interaction_mode(self, prompt_section: Optional[UserPromptSection] = None) -> Optional[type]:
        if prompt_section:
            if prompt_section.command == SUBJECT_DEFAULT_INVESTIGATE:
                return InvestigationInteractionMode
            elif prompt_section.command == SUBJECT_DEFAULT_FORMAT:
                return FormatedDataInteractionMode

        return DefaultInteractionMode

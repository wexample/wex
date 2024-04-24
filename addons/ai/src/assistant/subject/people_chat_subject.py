from typing import Optional

from addons.ai.src.assistant.interaction_mode.formated_data_interaction_mode import FORMATED_DATA_FORMATS
from addons.ai.src.assistant.interaction_mode.vetting_interaction_mode import VettingInteractionMode
from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict

SUBJECT_PEOPLE_COMMAND_VET = "vet"


class PeopleChatSubject(AbstractChatSubject):
    @staticmethod
    def name() -> str:
        return "people"

    def get_commands(self) -> StringKeysDict:
        return {
            SUBJECT_PEOPLE_COMMAND_VET: {
                "description": "Vet a people based on given data",
                "options": FORMATED_DATA_FORMATS
            },
        }

    def get_interaction_mode(self, prompt_section: Optional[UserPromptSection] = None) -> Optional[type]:
        return VettingInteractionMode

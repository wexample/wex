from typing import Optional, List

from langchain_community.vectorstores.chroma import Chroma

from addons.ai.src.assistant.subject.default_chat_subject import DefaultSubject
from addons.ai.src.assistant.utils.globals import AI_IDENTITY_INVESTIGATOR
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict

SUBJECT_INVESTIGATE_COMMAND_INVESTIGATE = "investigate"


class InvestigateChatSubject(DefaultSubject):
    chroma: Optional[Chroma] = None
    file_path: Optional[str] = None

    @staticmethod
    def name() -> str:
        return "investigate"

    def introduce(self) -> str:
        return f"Investigate a given problem by asking questions"

    def get_completer_commands(self) -> StringKeysDict:
        commands = {
            SUBJECT_INVESTIGATE_COMMAND_INVESTIGATE: "Investigate a problem",
        }

        return commands

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[bool | str]:
        return super().process_user_input(
            prompt_section,
            # Enforce identity
            self.assistant.identities[AI_IDENTITY_INVESTIGATOR],
            identity_parameters,
            remaining_sections,
        )

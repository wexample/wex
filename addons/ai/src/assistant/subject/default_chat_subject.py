from typing import Optional, List

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict


class DefaultSubject(AbstractChatSubject):
    @staticmethod
    def name() -> str:
        return "default"

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict,
        remaining_sections: List[UserPromptSection]
    ) -> Optional[bool | str]:
        self.assistant.spinner.start()

        response = self.assistant.get_default_model().chat(
            prompt_section.prompt,
            identity,
            identity_parameters or {},
        )

        self.assistant.spinner.stop()

        return response

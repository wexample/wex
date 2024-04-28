from typing import List, Optional, cast

import pyperclip

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.history_item import HistoryItem
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict

SUBJECT_PREVIOUS_RESPONSE_COMMAND_COPY_TO_CLIPBOARD = "copy_to_clipboard"


class PreviousResponseSubject(AbstractChatSubject):
    @staticmethod
    def name() -> str:
        return "previous_response"

    def introduce(self) -> str:
        return f"Reusing previous response"

    def get_commands(self) -> StringKeysDict:
        items = {}

        if len(self.assistant.history):
            items[
                SUBJECT_PREVIOUS_RESPONSE_COMMAND_COPY_TO_CLIPBOARD
            ] = "Copy previous response to clipboard"

        return items

    def process_prompt_section(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection],
    ) -> Optional[bool | str]:
        if (
            prompt_section.command
            == SUBJECT_PREVIOUS_RESPONSE_COMMAND_COPY_TO_CLIPBOARD
        ):
            if len(self.assistant.history):
                item = self.assistant.history[-1]
                pyperclip.copy(cast(HistoryItem, item).content)
                self.assistant.log(f"Previous response copied to clipboard")

        return True

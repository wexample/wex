from typing import Optional, List, cast

import pyperclip

from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse
from addons.ai.src.assistant.interaction_response.string_interaction_response import StringInteractionResponse
from addons.ai.src.assistant.utils.history_item import HistoryItem


class CopyClipboardCommand(AbstractCommand):
    description: str = "Copy previous response to clipboard"

    @staticmethod
    def name() -> str:
        return "copy-clipboard"

    def execute(
        self,
        prompt_section: Optional["UserPromptSection"] = None,
        remaining_sections: Optional[List["UserPromptSection"]] = None
    ) -> AbstractInteractionResponse:
        if len(self.assistant.history) > 1:
            # The direct previous item is the actual command,
            # so we take the second previous one.
            item = cast(HistoryItem, self.assistant.history[-2])

            if item and item.message:
                pyperclip.copy(cast(HistoryItem, item).message)
                return StringInteractionResponse("Previous response copied to clipboard")

        return StringInteractionResponse("No history items found")

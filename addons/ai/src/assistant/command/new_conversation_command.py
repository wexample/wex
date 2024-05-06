from typing import TYPE_CHECKING, List, Optional

from addons.ai.src.assistant.command.default_command import DefaultCommand
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse
from addons.ai.src.assistant.interaction_response.null_interaction_response import NullInteractionResponse

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class NewConversationCommand(DefaultCommand):
    description: str = "Start a new conversation"

    @staticmethod
    def name() -> str:
        return "new-conversation"

    def execute(
        self,
        prompt_section: Optional["UserPromptSection"] = None,
        remaining_sections: Optional[List["UserPromptSection"]] = None
    ) -> AbstractInteractionResponse:
        self.assistant.set_conversation()

        return NullInteractionResponse()

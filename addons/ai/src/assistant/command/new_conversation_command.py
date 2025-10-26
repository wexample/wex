from __future__ import annotations

from typing import TYPE_CHECKING

from addons.ai.src.assistant.command.default_command import DefaultCommand
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import (
    AbstractInteractionResponse,
)

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class NewConversationCommand(DefaultCommand):
    description: str = "Start a new conversation"

    @staticmethod
    def name() -> str:
        return "new-conversation"

    def execute(
        self,
        prompt_section: UserPromptSection | None = None,
        remaining_sections: list[UserPromptSection] | None = None,
    ) -> AbstractInteractionResponse:
        from addons.ai.src.assistant.interaction_response.null_interaction_response import (
            NullInteractionResponse,
        )

        self.assistant.set_conversation()

        return NullInteractionResponse()

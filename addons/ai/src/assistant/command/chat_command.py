from typing import TYPE_CHECKING, Type

from addons.ai.src.assistant.command.default_command import DefaultCommand
from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import (
    AbstractInteractionMode,
)
from addons.ai.src.assistant.interaction_mode.chat_interaction_mode import (
    ChatInteractionMode,
)

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class ChatCommand(DefaultCommand):
    description: str = "Short chat response"
    sticky: bool = True
    root_only: bool = True

    @staticmethod
    def name() -> str:
        return "chat"

    def get_interaction_mode(
        self, prompt_section: "UserPromptSection"
    ) -> Type[AbstractInteractionMode]:
        return ChatInteractionMode

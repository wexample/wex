from typing import Type, TYPE_CHECKING, Optional

from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import AbstractInteractionMode
from addons.ai.src.assistant.interaction_mode.chat_interaction_mode import ChatInteractionMode
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse
from addons.ai.src.assistant.interaction_response.string_interaction_response import StringInteractionResponse

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class ChatCommand(AbstractCommand):
    description: str = "Short chat response"
    sticky: bool = True
    root_only: str = True

    @staticmethod
    def name() -> str:
        return "chat"

    def get_interaction_mode(self, prompt_section: "UserPromptSection") -> Type[AbstractInteractionMode]:
        return ChatInteractionMode

    def execute(self, prompt_section: Optional["UserPromptSection"] = None) -> AbstractInteractionResponse:
        return StringInteractionResponse("YAY")

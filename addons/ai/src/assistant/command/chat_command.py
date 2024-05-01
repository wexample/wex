from typing import Type, TYPE_CHECKING

from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import AbstractInteractionMode
from addons.ai.src.assistant.interaction_mode.chat_interaction_mode import ChatInteractionMode

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class ChatCommand(AbstractCommand):
    @staticmethod
    def name() -> str:
        return "chat"

    def get_interaction_mode(self, prompt_section: "UserPromptSection") -> Type[AbstractInteractionMode]:
        return ChatInteractionMode

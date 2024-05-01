from typing import TYPE_CHECKING

from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse
from addons.ai.src.assistant.interaction_response.null_interaction_response import NullInteractionResponse


if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection

class MenuCommand(AbstractCommand):
    @staticmethod
    def name() -> str:
        return "menu"

    def execute(self, prompt_section: "UserPromptSection") -> AbstractInteractionResponse:
        print("MENU")

        return NullInteractionResponse()

from typing import TYPE_CHECKING

from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse
from addons.ai.src.assistant.interaction_response.prompt_exit_interaction_response import PromptExitInteractionResponse
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class ExitCommand(AbstractCommand):
    @staticmethod
    def name() -> str:
        return "exit"

    def execute(self, prompt_section: "UserPromptSection") -> AbstractInteractionResponse:
        return PromptExitInteractionResponse()

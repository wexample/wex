import os
from typing import Optional, TYPE_CHECKING, List

from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse
from addons.ai.src.assistant.interaction_response.string_interaction_response import StringInteractionResponse
from src.helper.command import execute_command_sync

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class TerminalCommand(AbstractCommand):
    description: str = "Execute command in the terminal"
    dir_path: Optional[str] = None

    @staticmethod
    def name() -> str:
        return "terminal"

    def execute(
        self,
        prompt_section: Optional["UserPromptSection"] = None,
        remaining_sections: Optional[List["UserPromptSection"]] = None
    ) -> AbstractInteractionResponse:
        success, response = execute_command_sync(
            self.kernel, prompt_section.prompt, ignore_error=True, shell=True
        )

        response_str = os.linesep.join(response)
        self.assistant.active_memory.add_message(response_str)

        return StringInteractionResponse(
            "Running: " + prompt_section.prompt + ":" + os.linesep + response_str
        )

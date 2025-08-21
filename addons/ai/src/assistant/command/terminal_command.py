import os
from typing import TYPE_CHECKING, List, Optional

from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import \
    AbstractInteractionResponse
from addons.ai.src.assistant.interaction_response.string_interaction_response import \
    StringInteractionResponse
from src.helper.command import execute_command_sync

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import \
        UserPromptSection


class TerminalCommand(AbstractCommand):
    description: str = "Execute command in the terminal"
    dir_path: Optional[str] = None

    @staticmethod
    def name() -> str:
        return "terminal"

    def execute(
        self,
        prompt_section: Optional["UserPromptSection"] = None,
        remaining_sections: Optional[List["UserPromptSection"]] = None,
    ) -> AbstractInteractionResponse:
        if prompt_section is None or prompt_section.prompt is None:
            return StringInteractionResponse("No command provided")

        cmd: str = prompt_section.prompt
        success, response = execute_command_sync(
            self.kernel, cmd, ignore_error=True, shell=True
        )

        response_str = os.linesep.join(response)
        self.assistant.set_history_item(response_str, "user")

        return StringInteractionResponse(
            "Running: " + cmd + ":" + os.linesep + response_str
        )

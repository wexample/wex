from typing import Optional, TYPE_CHECKING, List

from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class SubjectCommand(AbstractCommand):
    description: str = "Change talk subject"

    @staticmethod
    def name() -> str:
        return "subject"

    def execute(
        self,
        prompt_section: Optional["UserPromptSection"] = None,
        remaining_sections: Optional[List["UserPromptSection"]] = None
    ) -> AbstractInteractionResponse:
        # TODO
        print("TODO")
        return super().execute(prompt_section)

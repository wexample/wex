from typing import Optional, TYPE_CHECKING, List, cast

from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class SubjectCommand(AbstractCommand):
    description: str = "Change talk subject"

    @staticmethod
    def name() -> str:
        return "subject"

    def get_flags(self) -> List[str]:
        return cast(List[str], self.assistant.subjects.keys())

    def execute(
        self,
        prompt_section: Optional["UserPromptSection"] = None,
        remaining_sections: Optional[List["UserPromptSection"]] = None
    ) -> AbstractInteractionResponse:
        if len(prompt_section.flags):
            self.assistant.set_subject(prompt_section.flags[-1], prompt_section)
            
        return super().execute(prompt_section)
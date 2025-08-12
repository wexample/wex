from typing import TYPE_CHECKING, List, Optional, cast

from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import (
    AbstractInteractionResponse,
)

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
        remaining_sections: Optional[List["UserPromptSection"]] = None,
    ) -> AbstractInteractionResponse:
        if prompt_section is not None and getattr(prompt_section, "flags", None):
            self.assistant.set_subject(prompt_section.flags[-1], prompt_section)

        return super().execute(prompt_section)

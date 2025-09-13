from __future__ import annotations

from typing import TYPE_CHECKING

from addons.ai.src.assistant.command.abstract_command import AbstractCommand
from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import (
    AbstractInteractionMode,
)
from addons.ai.src.assistant.interaction_mode.default_interaction_mode import (
    DefaultInteractionMode,
)
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import (
    AbstractInteractionResponse,
)

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class DefaultCommand(AbstractCommand):
    description: str = "Default interaction with model"

    @staticmethod
    def name() -> str:
        return "default"

    def execute(
        self,
        prompt_section: UserPromptSection | None = None,
        remaining_sections: list[UserPromptSection] | None = None,
    ) -> AbstractInteractionResponse:
        if prompt_section is None:
            # Fallback: nothing to process
            return super().execute(prompt_section, remaining_sections)

        interaction_mode = self.get_interaction_mode(prompt_section)

        return interaction_mode(self.assistant).process_user_input(
            prompt_section=prompt_section,
            remaining_sections=remaining_sections or [],
        )

    def get_interaction_mode(
        self, prompt_section: UserPromptSection
    ) -> type[AbstractInteractionMode]:
        return DefaultInteractionMode

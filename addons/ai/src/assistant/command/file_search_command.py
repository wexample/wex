from __future__ import annotations

from typing import TYPE_CHECKING

from addons.ai.src.assistant.command.default_command import DefaultCommand
from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import (
    AbstractInteractionMode,
)

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class FileSearchCommand(DefaultCommand):
    description: str = "Similarity search into file"
    root_only: bool = True

    @staticmethod
    def name() -> str:
        return "file-search"

    def get_interaction_mode(
        self, prompt_section: UserPromptSection
    ) -> type[AbstractInteractionMode]:
        from addons.ai.src.assistant.interaction_mode.file_search_interaction_mode import (
            FileSearchInteractionMode,
        )

        return FileSearchInteractionMode

    def is_active(self, current_prompt: str) -> bool:
        from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject

        return isinstance(self.assistant.subject, FileChatSubject)

from typing import TYPE_CHECKING, Type

from addons.ai.src.assistant.command.default_command import DefaultCommand
from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import \
    AbstractInteractionMode
from addons.ai.src.assistant.interaction_mode.dir_search_interaction_mode import \
    DirSearchInteractionMode
from addons.ai.src.assistant.subject.dir_chat_subject import DirChatSubject

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import \
        UserPromptSection


class DirSearchCommand(DefaultCommand):
    description: str = "Similarity search into directory"
    root_only: bool = True

    @staticmethod
    def name() -> str:
        return "dir-search"

    def is_active(self, current_prompt: str) -> bool:
        return isinstance(self.assistant.subject, DirChatSubject)

    def get_interaction_mode(
        self, prompt_section: "UserPromptSection"
    ) -> Type[AbstractInteractionMode]:
        return DirSearchInteractionMode

from typing import TYPE_CHECKING, Type

from addons.ai.src.assistant.command.default_command import DefaultCommand
from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject
from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import AbstractInteractionMode
from addons.ai.src.assistant.interaction_mode.file_rewrite_interaction_mode import FileRewriteInteractionMode

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class FileRewriteCommand(DefaultCommand):
    description: str = "Rewrite a file following given guidelines"
    root_only: str = True

    @staticmethod
    def name() -> str:
        return "file-rewrite"

    def is_active(self, current_prompt: str) -> bool:
        return isinstance(self.assistant.subject, FileChatSubject)

    def get_interaction_mode(self, prompt_section: "UserPromptSection") -> Type[AbstractInteractionMode]:
        return FileRewriteInteractionMode

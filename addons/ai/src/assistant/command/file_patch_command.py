from typing import TYPE_CHECKING, Type

from addons.ai.src.assistant.command.default_command import DefaultCommand
from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import \
    AbstractInteractionMode
from addons.ai.src.assistant.interaction_mode.file_patch_interaction_mode import \
    FilePatchInteractionMode
from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject

if TYPE_CHECKING:
    from addons.ai.src.assistant.utils.user_prompt_section import \
        UserPromptSection


class FilePatchCommand(DefaultCommand):
    description: str = "Create a patch an apply it to file"
    root_only: bool = True

    @staticmethod
    def name() -> str:
        return "file-patch"

    def is_active(self, current_prompt: str) -> bool:
        return isinstance(self.assistant.subject, FileChatSubject)

    def get_interaction_mode(
        self, prompt_section: "UserPromptSection"
    ) -> Type[AbstractInteractionMode]:
        return FilePatchInteractionMode

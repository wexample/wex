import os.path
from typing import Optional

from addons.ai.src.assistant.subject.abstract_chat_subject import \
    AbstractChatSubject
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict
from src.helper.prompt import prompt_pick_a_file

SUBJECT_FILE_CHAT_COMMAND_PATCH = "patch"
SUBJECT_FILE_CHAT_COMMAND_TALK_ABOUT_FILE = "talk_about_file"


class FileChatSubject(AbstractChatSubject):
    file_path: Optional[str] = None

    @staticmethod
    def name() -> str:
        return "file"

    def introduce(self) -> str:
        return f"Chatting about file {self.file_path}"

    def activate(self, prompt_section: Optional[UserPromptSection] = None) -> bool:
        if super().activate():
            user_input = prompt_section.prompt if prompt_section else None
            user_input_trimmed = user_input.strip() if user_input else None

            file_path: Optional[str]
            if user_input_trimmed and os.path.isfile(user_input_trimmed):
                file_path = user_input_trimmed
            else:
                file_path = prompt_pick_a_file()

                if not file_path:
                    self.assistant.log("No file selected")
                    return False

            if not file_path:
                self.assistant.log(f"File not found {file_path}")
                return False

            self.set_file_path(file_path)
            return True

        return False

    def set_file_path(self, file_path: str) -> None:
        real = os.path.realpath(file_path)
        if not real:
            return
        self.file_path = real

    # Test helper: expose examples loader through the subject API for convenience.
    def load_example_patch(self, name: str) -> StringKeysDict:
        from addons.ai.src.assistant.interaction_mode.file_patch_interaction_mode import \
            FilePatchInteractionMode

        # Delegate to the interaction mode implementation
        return FilePatchInteractionMode(self.assistant).load_example_patch(name)

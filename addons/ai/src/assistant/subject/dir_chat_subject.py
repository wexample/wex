import os
from typing import Optional, List

from addons.ai.src.assistant.interaction_mode.dir_search_interaction_mode import DirSearchInteractionMode
from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict
from src.helper.prompt import prompt_pick_a_dir

SUBJECT_FILE_CHAT_COMMAND_TALK_ABOUT_DIR = "talk_about_dir"


class DirChatSubject(AbstractChatSubject):
    dir_path: Optional[str] = None

    @staticmethod
    def name() -> str:
        return "dir"

    def get_interaction_modes(self) -> List[type]:
        return [
            DirSearchInteractionMode,
        ]

    def introduce(self) -> str:
        return f"Chatting about all files in given directory {self.dir_path}"

    def get_commands(self) -> StringKeysDict:
        return {
            SUBJECT_FILE_CHAT_COMMAND_TALK_ABOUT_DIR: "Talk about file",
        }

    def activate(self, prompt_section: Optional[UserPromptSection] = None) -> bool:
        if super().activate():
            user_input = prompt_section.prompt if prompt_section else None
            user_input_trimmed = user_input.strip() if user_input else None

            if user_input_trimmed and os.path.isfile(user_input_trimmed):
                dir_path = user_input_trimmed
            else:
                dir_path = prompt_pick_a_dir()

                if not dir_path:
                    self.assistant.log("No file selected")
                    return False

            if not dir_path:
                self.assistant.log(f"File not found {dir_path}")
                return False

            self.set_dir_path(dir_path)
            return True

        return False

    def set_dir_path(self, dir_path: str) -> None:
        dir_path = os.path.realpath(dir_path)

        if not dir_path:
            return None

        self.dir_path = dir_path

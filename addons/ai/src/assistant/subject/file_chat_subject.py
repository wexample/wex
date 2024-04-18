import os.path
from typing import Optional, List

from addons.ai.src.assistant.interaction_mode.file_explore_interaction_mode import FileExploreInteractionMode
from addons.ai.src.assistant.interaction_mode.file_patch_interaction_mode import FilePatchInteractionMode
from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict
from src.helper.dict import dict_merge, dict_sort_values
from src.helper.file import file_read_if_exists
from src.helper.prompt import prompt_choice_dict
from src.helper.string import string_add_lines_numbers

SUBJECT_FILE_CHAT_COMMAND_PATCH = "patch"
SUBJECT_FILE_CHAT_COMMAND_TALK_ABOUT_FILE = "talk_about_file"


class FileChatSubject(AbstractChatSubject):
    file_path: Optional[str] = None

    @staticmethod
    def name() -> str:
        return "file"

    def get_interaction_modes(self) -> List[type]:
        return [
            FileExploreInteractionMode,
            FilePatchInteractionMode,
        ]

    def introduce(self) -> str:
        return f"Chatting about file {self.file_path}"

    def get_completer_commands(self) -> StringKeysDict:
        commands = {
            SUBJECT_FILE_CHAT_COMMAND_TALK_ABOUT_FILE: "Talk about file",
        }

        if self.is_current_subject():
            commands[SUBJECT_FILE_CHAT_COMMAND_PATCH] = "Modify file"

        return commands

    def activate(self, prompt_section: Optional[UserPromptSection] = None) -> bool:
        if super().activate():
            user_input = prompt_section.prompt if prompt_section else None
            user_input_trimmed = user_input.strip() if user_input else None

            if user_input_trimmed and os.path.isfile(user_input_trimmed):
                file_path = user_input_trimmed
            else:
                file_path = self.pick_a_file()

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
        file_path = os.path.realpath(file_path)

        if not file_path:
            return None

        self.file_path = file_path

    def pick_a_file(self, base_dir: Optional[str] = None) -> Optional[str]:
        base_dir = base_dir or os.getcwd()
        # Use two dicts to keep dirs and files separated ignoring emojis in alphabetical sorting.
        choices_dirs = {"..": ".."}
        choices_files = {}

        for element in os.listdir(base_dir):
            if os.path.isdir(os.path.join(base_dir, element)):
                element_label = f"📁 {element}"
                choices_dirs[element] = element_label
            else:
                element_label = element
                choices_files[element] = element_label

        choices_dirs = dict_sort_values(choices_dirs)
        choices_files = dict_sort_values(choices_files)

        file = prompt_choice_dict(
            "Select a file to talk about:",
            dict_merge(choices_dirs, choices_files),
        )

        if file:
            full_path = os.path.join(base_dir, file)
            if os.path.isfile(full_path):
                return full_path
            elif os.path.isdir(full_path):
                self.pick_a_file(full_path)

        return None

    def load_example_patch(self, name) -> StringKeysDict:
        base_path = f"{self.kernel.directory.path}addons/ai/samples/examples/{name}/"
        source = file_read_if_exists(f"{base_path}source.txt")

        return {
            "file_name": "file_name.py",
            "question": file_read_if_exists(f"{base_path}question.txt"),
            "source": source,
            "source_with_lines": string_add_lines_numbers(source) if source else None,
            "response": file_read_if_exists(f"{base_path}response.patch"),
        }

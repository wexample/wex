import os.path
from typing import Optional

import patch
from langchain_community.vectorstores.chroma import Chroma

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.identities import AI_IDENTITY_FILE_INSPECTION
from addons.ai.src.model.open_ai_model import MODEL_NAME_OPEN_AI_GPT_4
from addons.default.helper.git_utils import git_file_get_octal_mode
from src.const.types import StringKeysDict, StringsList
from src.helper.dict import dict_merge, dict_sort_values
from src.helper.dir import dir_execute_in_workdir
from src.helper.file import file_read, file_read_if_exists, file_set_user_or_sudo_user_owner
from src.helper.patch import patch_is_valid
from src.helper.prompt import prompt_choice_dict
from src.helper.string import string_add_lines_numbers, string_has_trailing_new_line

SUBJECT_FILE_CHAT_COMMAND_PATCH = "patch"
SUBJECT_FILE_CHAT_COMMAND_TALK_ABOUT_FILE = "talk_about_file"


class FileChatSubject(AbstractChatSubject):
    chroma: Optional[Chroma] = None
    file_path: Optional[str] = None

    @staticmethod
    def name() -> str:
        return "file"

    def introduce(self) -> str:
        return f"Chatting about file {self.file_path}"

    def get_completer_commands(self) -> StringsList:
        commands = [SUBJECT_FILE_CHAT_COMMAND_TALK_ABOUT_FILE]

        if self.is_current_subject():
            commands.append(SUBJECT_FILE_CHAT_COMMAND_PATCH)

        return commands

    def process_user_input(
        self,
        user_input_split: StringKeysDict,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict,
    ) -> Optional[str]:
        user_command = user_input_split["command"]
        user_input = user_input_split["input"]
        path = self.file_path

        if user_command == SUBJECT_FILE_CHAT_COMMAND_PATCH:
            # Avoid empty input error.
            if not user_input:
                return f'Please instruct how to patch this file {path}'

            model = self.assistant.get_model()
            file_name = os.path.basename(path)
            file_content = file_read(path)
            file_content_with_numbers = string_add_lines_numbers(file_content)
            patch_content = (
                f"diff --git a/{file_name} b/{file_name}"
                f"\nindex 1234567..abcdefg {git_file_get_octal_mode(path)}"
                f"\n--- a/{file_name}"
                f"\n+++ b/{file_name}"
                f"\n"
            )

            identity_parameters.update(
                {
                    "file_name": file_name,
                    "question": user_input,
                    "source": file_content_with_numbers,
                }
            )

            patch_content += (
                model.chat_with_few_shots(
                    user_input=user_input,
                    identity=identity,
                    identity_parameters=identity_parameters,
                    example_prompt=(
                        "User request:\n{question}\n\n"
                        "File name:\n{file_name}\n\n"
                        "Complete source code of the application:\n{source}\n\n"
                        "AI-generated Git patch:\n"
                    ),
                    examples=[
                        self.load_example_patch("generate/program_hello_world"),
                        self.load_example_patch("explain/code_comment"),
                        self.load_example_patch("patch/hello_world_capitalized"),
                    ],
                )
                + os.linesep
            )

            error_message = "Generated patch body is not valid"
            if patch_is_valid(patch_content):
                # This notation is a patch standard
                if not string_has_trailing_new_line(file_content):
                    patch_content = (
                        patch_content.rstrip() + "\n\\ No newline at end of file"
                    )

                patch_set = patch.fromstring(patch_content.encode())
                error_message = "Unable to create patch set"
                if patch_set:
                    def _patch_it():
                        nonlocal error_message

                        error_message = "File can't be patched"
                        return patch_set.apply()

                    # Patch library expect patch to refer to a relative file,
                    # so we move in the same dir.
                    success = dir_execute_in_workdir(os.path.dirname(path), _patch_it)
                    error_message = "Patching failed"

                    if success:
                        file_set_user_or_sudo_user_owner(path)

                        return f'✏️ Patched : {path}'

            return f'⚠️ {error_message}: \n{patch_content}'

        elif user_command == SUBJECT_FILE_CHAT_COMMAND_TALK_ABOUT_FILE:
            self.set_file_path(
                self.pick_a_file()
            )

        # Talking about a file and initialized.
        if self.chatting_ready():
            # Avoid empty input error.
            if not user_input:
                return f'Please ask something about the file {path}'

            results = self.chroma.similarity_search_with_relevance_scores(
                user_input, k=3, filter={"source": self.file_path}
            )

            return self.assistant.get_model().chat(
                user_input,
                self.assistant.identities[AI_IDENTITY_FILE_INSPECTION],
                identity_parameters
                or {
                    "context": "\n\n---\n\n".join(
                        [doc.page_content for doc, _score in results]
                    )
                },
            )

        return None

    def set_file_path(self, file_path: str) -> None:
        if not file_path:
            return 'No file selected'

        self.file_path = file_path
        self.assistant.vector_store_file(self.file_path)
        self.assistant.set_subject(self.name())

        embedding_function = self.assistant.get_model(
            MODEL_NAME_OPEN_AI_GPT_4
        ).create_embeddings()

        self.chroma = Chroma(
            persist_directory=self.assistant.chroma_path,
            embedding_function=embedding_function,
            collection_name="single_files",
        )

    def chatting_ready(self) -> bool:
        return self.is_current_subject() and self.chroma and self.file_path

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

    def load_example_patch(self, name):
        base_path = f"{self.kernel.directory.path}addons/ai/samples/examples/{name}/"
        source = file_read_if_exists(f"{base_path}source.py")

        return {
            "file_name": "file_name.py",
            "question": file_read_if_exists(f"{base_path}question.txt"),
            "source": string_add_lines_numbers(source) if source else None,
            "patch": file_read_if_exists(f"{base_path}response.patch"),
        }

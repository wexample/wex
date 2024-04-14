import os.path
from typing import Optional

import patch
from langchain_community.vectorstores.chroma import Chroma

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.globals import AI_IDENTITY_FILE_INSPECTION
from addons.ai.src.model.open_ai_model import MODEL_NAME_OPEN_AI_GPT_4
from addons.default.helper.git_utils import git_file_get_octal_mode
from src.const.types import StringKeysDict
from src.helper.dict import dict_merge, dict_sort_values
from src.helper.file import file_read, file_read_if_exists, file_set_user_or_sudo_user_owner, file_get_extension
from src.helper.patch import patch_is_valid, patch_apply_in_workdir, extract_information, patch_clean, \
    patch_create_hunk_header
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

    def get_completer_commands(self) -> StringKeysDict:
        commands = {
            SUBJECT_FILE_CHAT_COMMAND_TALK_ABOUT_FILE: "Talk about file",
        }

        if self.is_current_subject():
            commands[SUBJECT_FILE_CHAT_COMMAND_PATCH] = "Modify file"

        return commands

    def process_user_input(
        self,
        user_input_split: StringKeysDict,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict,
    ) -> Optional[str]:
        user_command = user_input_split["command"]
        user_input = user_input_split["input"]
        file_path = self.file_path

        if user_command == SUBJECT_FILE_CHAT_COMMAND_PATCH:
            # Avoid empty input error.
            if not user_input:
                return f'Please instruct what to change in this file {file_path}'

            # Per file format system prompt.
            extension = file_get_extension(file_path)
            if extension == "json":
                identity["system"] += \
                    ("\nAs this is a JSON file, you respect these rules :"
                     "\n  - Adding a comma in the end of line should also be reflected as a line change."
                     "\n  - Also the last item of a json dict should not have a comma in the end of line.")

            model = self.assistant.get_default_model()
            file_name = os.path.basename(file_path)
            # Strip the original file to prevent having to fix mismatches.
            file_content = file_read(file_path).strip()
            source_with_lines = string_add_lines_numbers(file_content)

            identity_parameters.update(
                {
                    "file_name": file_name,
                    "question": user_input,
                    "source_with_lines": source_with_lines,
                }
            )

            self.assistant.spinner.start()

            raw_patch_content = (
                model.chat_with_few_shots(
                    user_input=user_input,
                    identity=identity,
                    identity_parameters=identity_parameters,
                    example_prompt=(
                        "User request:\n{question}\n\n"
                        "File name:\n{file_name}\n\n"
                        "Complete source code of the application:\n{source_with_lines}\n\n"
                        "AI-generated Git patch:\n"
                    ),
                    examples=[
                        self.load_example_patch("generate/program_hello_world"),
                        self.load_example_patch("explain/code_comment"),
                        self.load_example_patch("patch/hello_world_capitalized"),
                        self.load_example_patch("json/add_item"),
                    ],
                    input_variables_names=["file_name", "question", "source_with_lines"]
                )
                + os.linesep
            )

            self.assistant.spinner.stop()

            description = extract_information(raw_patch_content, "DESCRIPTION", "No description")

            # Patch content
            patch_content = patch_clean(raw_patch_content)
            hunk_header = patch_create_hunk_header(file_content, patch_content)

            error_message = "Unable to generate hunk header"
            if hunk_header:
                error_message = "Generated patch body is not valid"
                patch_content = hunk_header + os.linesep + patch_content

                if patch_is_valid(patch_content):
                    # Add headers that help applying patch
                    patch_content = (
                        f"diff --git a/{file_name} b/{file_name}"
                        f"\nindex 1234567..abcdefg {git_file_get_octal_mode(file_path)}"
                        f"\n--- a/{file_name}"
                        f"\n+++ b/{file_name}"
                        f"\n" + patch_content
                    )

                    # This notation is a patch standard
                    if not string_has_trailing_new_line(file_content):
                        patch_content = (
                            patch_content.rstrip() + "\n\\ No newline at end of file"
                        )

                    patch_set = patch.fromstring(patch_content.encode())
                    error_message = "Unable to create patch set"

                    if patch_set:
                        # Patch library expect patch to refer to a relative file,
                        # so we move in the same dir.
                        success = patch_apply_in_workdir(os.path.dirname(file_path), patch_set)
                        error_message = "Patching failed"
                        if success:
                            file_set_user_or_sudo_user_owner(file_path)
                            self.kernel.io.log(f'Patched : {file_path}')

                            return f'✏️ {description}'

                    self.kernel.io.log(file_content)
                    self.kernel.io.log("____")
                    self.kernel.io.log(patch_content)
                else:
                    self.kernel.io.log(file_content)
                    self.kernel.io.log("____")
                    self.kernel.io.log(raw_patch_content)
            else:
                self.kernel.io.log(file_content)
                self.kernel.io.log("____")
                self.kernel.io.log(patch_content)

            return f'⚠️ {error_message}'

        elif user_command == SUBJECT_FILE_CHAT_COMMAND_TALK_ABOUT_FILE:
            user_input_trimmed = user_input.strip() if user_input else None

            if user_input_trimmed and os.path.isfile(user_input_trimmed):
                file_path = user_input_trimmed
                user_input = None
            else:
                file_path = self.pick_a_file()

                if not file_path:
                    return 'No file selected'

            self.set_file_path(file_path)

            if not self.file_path:
                return f'File not found {file_path}'

            file_path = self.file_path

        # Talking about a file and initialized.
        if self.chatting_ready():
            # Avoid empty input error.
            if not user_input:
                return f'Please ask something about the file {file_path}'

            results = self.chroma.similarity_search_with_relevance_scores(
                user_input, k=3, filter={"source": self.file_path}
            )

            self.assistant.spinner.start()

            response = self.assistant.get_default_model().chat(
                user_input,
                self.assistant.identities[AI_IDENTITY_FILE_INSPECTION],
                identity_parameters
                or {
                    "context": "\n\n---\n\n".join(
                        [doc.page_content for doc, _score in results]
                    )
                },
            )

            self.assistant.spinner.stop()

            return response

        return None

    def set_file_path(self, file_path: str) -> None:
        file_path = os.path.realpath(file_path)

        if not file_path:
            return None

        self.file_path = file_path
        self.assistant.vector_store_file(self.file_path)
        self.assistant.set_subject(self.name())

        embedding_function = self.assistant.get_default_model(
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

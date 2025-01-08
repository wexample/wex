import os
from typing import List, Optional, cast

import patch
from wexample_helpers.helpers.file import file_read

from addons.ai.src.assistant.interaction_mode.abstract_interaction_mode import (
    AbstractInteractionMode,
)
from addons.ai.src.assistant.interaction_response.abstract_interaction_response import AbstractInteractionResponse
from addons.ai.src.assistant.interaction_response.string_interaction_response import StringInteractionResponse
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from addons.default.helper.git_utils import git_file_get_octal_mode
from src.const.types import StringKeysDict
from src.helper.file import (
    file_get_extension,
    file_read_if_exists,
    file_set_user_or_sudo_user_owner,
)
from src.helper.patch import (
    extract_information,
    patch_apply_in_workdir,
    patch_clean,
    patch_create_hunk_header,
    patch_is_valid,
)
from src.helper.string import string_add_lines_numbers, string_has_trailing_new_line


class FilePatchInteractionMode(AbstractInteractionMode):
    @staticmethod
    def name() -> str:
        return "file_patch"

    def get_initial_prompt(self, prompt_section: UserPromptSection) -> Optional[str]:
        return (
            "You generate file diffs in unidiff format based on user instructions, and wrapped into a json object."
            '\nStart the patch with "# PATCH_START" then the patch content without header.'
            "\nThe patch body always starts 3 lines before the first change, "
            "if applicable, this is the security margin."
            "\nYou respect the exact original spacings, indentation."
            "\nYou do not do any change without marking it with a + or a -."
            "\nTerminate with the # DESCRIPTION: information describing what you've done."
        )

    def process_user_input(
        self,
        prompt_section: UserPromptSection,
        remaining_sections: List[UserPromptSection],
    ) -> AbstractInteractionResponse:
        from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject

        user_input = prompt_section.prompt
        subject = cast(FileChatSubject, self.assistant.get_current_subject())
        file_path = subject.file_path

        # Avoid empty input error.
        if not user_input:
            return StringInteractionResponse(f"Please instruct what to change in this file {file_path}")

        # Per file format system prompt.
        extension = file_get_extension(file_path)
        if extension == "json":
            prompt_section.prompt_configurations.append(
                (
                    "system",
                    "As this is a JSON file, you respect these rules :"
                    "\n  - Adding a comma in the end of line should also be reflected as a line change."
                    "\n  - Also the last item of a json dict should not have a comma in the end of line."
                )
            )

        model = self.assistant.get_model()
        file_name = os.path.basename(file_path)
        # Strip the original file to prevent having to fix mismatches.
        file_content = file_read(file_path).strip()
        source_with_lines = string_add_lines_numbers(file_content)

        self.assistant.spinner.start()

        raw_patch_content = (
            model.chat_with_few_shots(
                interaction_mode=self,
                prompt_section=prompt_section,
                prompt_parameters={
                    "file_name": file_name,
                    "question": user_input,
                    "source_with_lines": source_with_lines,
                },
                example_prompt=(
                    "User request:\n{question}\n\n"
                    "File name:\n{file_name}\n\n"
                    "File content:\n{source_with_lines}\n\n"
                    "AI-generated Git patch:\n"
                ),
                examples=[
                    self.load_example_patch("generate/program_hello_world"),
                    self.load_example_patch("explain/code_comment"),
                    self.load_example_patch("patch/hello_world_capitalized"),
                    self.load_example_patch("json/add_item"),
                ],
                input_variables_names=["file_name", "question", "source_with_lines"],
            )
            + os.linesep
        )

        self.assistant.spinner.stop()

        description = extract_information(
            raw_patch_content, "DESCRIPTION", "No description"
        )

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
                    success = patch_apply_in_workdir(
                        os.path.dirname(file_path), patch_set
                    )
                    error_message = "Patching failed"
                    if success:
                        file_set_user_or_sudo_user_owner(file_path)
                        self.kernel.io.log(f"Patched : {file_path}")

                        return StringInteractionResponse(f"✏️ {description}")

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

        return StringInteractionResponse(f"⚠️ {error_message}")

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

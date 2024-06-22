import enum
import os
from typing import Dict, cast, List

import patch
from langchain_core.prompts import FewShotPromptTemplate
from wexample_helpers.helpers.file_helper import file_write, file_read

from addons.ai.helper.chat import TEXT_ALIGN_RIGHT, chat_format_message
from addons.ai.src.assistant.assistant import (
    AI_COMMAND_PREFIX,
    Assistant,
)
from addons.ai.src.assistant.command.exit_command import ExitCommand
from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject
from addons.ai.src.model.ollama_model import MODEL_NAME_OLLAMA_MISTRAL
from addons.ai.src.assistant.command.chat_command import ChatCommand
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection
from src.const.types import StringKeysDict
from src.helper.package import package_enable_logging
from src.helper.patch import (
    patch_apply_in_workdir,
    patch_clean,
    patch_create_hunk_header,
    patch_find_line_of_first_subgroup,
    patch_get_initial_lines,
    patch_get_initial_parts,
    patch_has_all_parts,
)
from tests.AbstractTestCase import AbstractTestCase


class TestAiCommandTalkAsk(AbstractTestCase):
    def test_ask(self) -> None:
        assistant = Assistant(self.kernel, MODEL_NAME_OLLAMA_MISTRAL)

        self._test_ask_parsing(assistant)
        # self._test_ask_formatting(assistant)
        # self._test_ask_assistant(assistant)
        # self._test_few_shot_prompt_template(assistant)
        # self._test_few_shot_examples(assistant)
        # self._test_diff(assistant)
        # self._test_patching(assistant)

    def _test_ask_parsing(self, assistant: Assistant) -> None:
        assistant.set_default_subject()

        self._found_one_command(
            assistant,
            ChatCommand.name(),
            f"/chat This is a short question",
            True
        )

        splits = self._found_one_command(
            assistant,
            "subject",
            f"/subject:file /this/is/a/path/to/file.txt",
            True
        )

        self.assertEqual(
            splits[0].prompt,
            "/this/is/a/path/to/file.txt"
        )

        for command in assistant.commands.values():
            # Fail expected
            if not isinstance(command, ExitCommand):
                command_name = command.name()

                self._found_one_command(assistant, command_name, f"{command_name}", False)
                self._found_one_command(assistant, command_name, f"Lorem{command_name}ipsum", False)
                self._found_one_command(assistant, command_name, f"Lorem{command_name}", False)
                self._found_one_command(assistant, command_name, f"{command_name}ipsum", False)
                self._found_one_command(
                    assistant, command_name, f"Lorem{AI_COMMAND_PREFIX}{command_name}ipsum", False
                )
                self._found_one_command(
                    assistant, command_name, f"Lorem{AI_COMMAND_PREFIX}{command_name}", False
                )
                self._found_one_command(
                    assistant, command_name, f"{AI_COMMAND_PREFIX}{command_name}ipsum", False
                )

                # Success expected
                self._found_one_command(
                    assistant, command_name, f"{AI_COMMAND_PREFIX}{command_name}", True
                )
                self._found_one_command(
                    assistant, command_name, f"Lorem {AI_COMMAND_PREFIX}{command_name}", True
                )
                self._found_one_command(
                    assistant, command_name, f"{AI_COMMAND_PREFIX}{command_name} ipsum", True
                )
                self._found_one_command(
                    assistant, command_name, f"Lorem {AI_COMMAND_PREFIX}{command_name} ipsum", True
                )

    def _found_one_command(
        self,
        assistant: Assistant,
        command: str,
        text: str,
        should_succeed: bool
    ) -> List[UserPromptSection]:
        user_input_splits = assistant.split_prompt_sections(text)

        success = any(
            user_input_split.has_command() and user_input_split.get_command().name() == command
            for user_input_split in user_input_splits
        )

        self.assertTrue(
            success == should_succeed,
            f'Command "{command}" found in text : "{text}"'
        )

        return user_input_splits

    def _test_ask_assistant(self, assistant: Assistant) -> None:
        assistant = Assistant(self.kernel, MODEL_NAME_OLLAMA_MISTRAL)

        self.assertGreater(len(assistant.personalities.values()), 1)

        test_ext = [
            "csv",
            "html",
            "json",
            "md",
            "pdf",
        ]

        assistant.set_subject(FileChatSubject.name())
        subject = assistant.get_current_subject()
        # interaction_mode = cast(
        #     FileSearchInteractionMode, subject.get_interaction_mode()(subject)
        # )

        # for ext in test_ext:
        #     sample_path = self.build_test_samples_path() + ext + "/simple." + ext
        #
        #     chunks = interaction_mode.vector_create_file_chunks(
        #         file_path=sample_path, file_signature=f"test-{ext}"
        #     )
        #
        #     self.assertTrue(len(chunks) > 0)

    def _test_ask_formatting(self, assistant: Assistant) -> None:
        message = chat_format_message(
            "Left align : Lorem ipsum dolor sit amet consecetur blah blah blah blah blah blah blah blah."
        )

        self.kernel.io.print(message)

        self.assertTrue(
            "+---" in message,
        )

        message = chat_format_message(
            "Right align : Lorem ipsum dolor sit amet consecetur blah blah blah blah blah blah blah blah.",
            align=TEXT_ALIGN_RIGHT,
            padding=2,
        )

        self.assertTrue(
            "+---" in message,
        )

        self.kernel.io.print(message)

    def _test_few_shot_prompt_template(self, assistant: Assistant) -> None:
        model = assistant.get_model()

        file_chat_subject = cast(
            FileChatSubject, assistant.subjects[FileChatSubject.name()]
        )

        template = model.create_few_shot_prompt_template(
            example_prompt=(
                "User request:\n{question}\n\n"
                "File name:\n{file_name}\n\n"
                "Complete source code of the application:\n{source}\n\n"
                "AI-generated Git patch:\n"
            ),
            examples=[
                file_chat_subject.load_example_patch("generate/program_hello_world"),
                file_chat_subject.load_example_patch("explain/code_comment"),
                file_chat_subject.load_example_patch("patch/hello_world_capitalized"),
                file_chat_subject.load_example_patch("json/add_item"),
            ],
            input_variables_names=["file_name", "question", "source_with_lines"],
        )

        self.assertTrue(isinstance(template, FewShotPromptTemplate))

    def _test_few_shot_examples(self, assistant: Assistant) -> None:
        examples = self._get_all_examples(assistant)
        for group in examples.values():
            for example, example_name in group.items():
                self.assertIsDict(
                    example, f'Example patch "{example_name}" has been loaded'
                )

    def _get_all_examples(self, assistant: Assistant) -> Dict[str, StringKeysDict]:
        examples = {}

        file_chat_subject = cast(
            FileChatSubject, assistant.subjects[FileChatSubject.name()]
        )

        base_dir = self.kernel.directory.path + "addons/ai/samples/examples/"
        for group_name in os.listdir(base_dir):
            examples[group_name] = {}

            for example_name in os.listdir(os.path.join(base_dir, group_name)):
                examples[group_name][
                    example_name
                ] = file_chat_subject.load_example_patch(f"{group_name}/{example_name}")

        return examples

    def _test_diff(self, assistant: Assistant) -> None:
        file_content = (
            "This is a demo file"
            "\nWith several lines"
            "\nSome empty lines"
            "\n"
            "\nSome other lines"
            "\n    And some other lines surrounded by spaces    "
            "\nAnd no ending line"
        )

        self.assertTrue(
            patch_has_all_parts(
                file_content,
                [
                    ["Some empty lines", ""],
                    ["    And some other lines surrounded by spaces    "],
                ],
            )
        )

        # This version does not support if spaces does not match.
        self.assertFalse(
            patch_has_all_parts(
                file_content,
                [
                    [" Some empty lines", " "],
                    [" And some other lines surrounded by spaces    "],
                ],
            )
        )

        self.assertEqual(
            patch_find_line_of_first_subgroup(
                file_content,
                [
                    ["Some empty lines", ""],
                ],
            ),
            3,
        )

        patch_content = (
            " This is a patch"
            "\n+With added line"
            "\n-With removed line"
            "\n "
            "\n And unchanged line"
        )

        self.assertEqual(len(patch_get_initial_lines(patch_content)), 4)

        patch_content = (
            "+This is a new line"
            "\n With a line starting with space"
            "\n-This line starts with a dash and should be in the first group"
            "\n+Another new line"
            "\n This should be in a separate group because it's separated by a '+' line"
            "\n-This line also starts with a dash and should be in the second group"
        )

        groups = patch_get_initial_parts(patch_content)

        self.assertEqual(len(groups), 2)

        self.assertEqual(len(groups[0]), 2)

        # Test examples
        examples = self._get_all_examples(assistant)
        for group in examples.values():
            for example in group.values():
                self.assertIsNotNone(
                    patch_create_hunk_header(
                        example["source"],
                        patch_clean(example["response"]),
                    )
                )

    def _test_patching(self, assistant: Assistant) -> None:
        target_package_json = (
            self.kernel.directory.path
            + "addons/ai/tests/resources/patches/target-package.json"
        )
        original_package_content = file_read(target_package_json)
        patches_dir = self.kernel.directory.path + "addons/ai/tests/resources/patches/"

        class PatchStatus(enum.Enum):
            LOAD_FAIL = 0
            LOAD_SUCCESS_APPLY_FAIL = 1
            LOAD_AND_APPLY_SUCCESS = 2

        # Mapping of patch files to their expected outcomes using the PatchStatus enum
        patch_files = {
            "package-random.patch": PatchStatus.LOAD_AND_APPLY_SUCCESS,
            "package-random-two.patch": PatchStatus.LOAD_FAIL,
            "package-random-three.patch": PatchStatus.LOAD_SUCCESS_APPLY_FAIL,
        }

        for patch_file, status in patch_files.items():
            patch_path = patches_dir + patch_file
            patch_data = file_read(patch_path).encode()
            patch_set = patch.fromstring(patch_data)

            package_enable_logging()

            # Check if the patch set is loaded properly
            if not patch_set:
                if status == PatchStatus.LOAD_FAIL:
                    self.assertTrue(
                        True, f"Patch {patch_file} expected to fail loading"
                    )
                else:
                    self.assertTrue(
                        False, f"Patch {patch_file} unexpectedly failed to load"
                    )
            else:
                if status == PatchStatus.LOAD_AND_APPLY_SUCCESS:
                    result = patch_apply_in_workdir(patches_dir, patch_set)
                    self.assertTrue(
                        result,
                        f"Patch {patch_file} expected to be valid and apply successfully",
                    )
                elif status == PatchStatus.LOAD_SUCCESS_APPLY_FAIL:
                    result = patch_apply_in_workdir(patches_dir, patch_set)
                    self.assertFalse(
                        result, f"Patch {patch_file} expected to load but fail to apply"
                    )

            # Restore the original package content after each patch test
            file_write(target_package_json, original_package_content)

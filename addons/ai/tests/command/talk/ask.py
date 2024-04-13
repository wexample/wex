import os
from typing import cast

import enum

import patch
from langchain_core.prompts import FewShotPromptTemplate

from addons.ai.helper.chat import TEXT_ALIGN_RIGHT, chat_format_message
from addons.ai.src.assistant.assistant import Assistant, ASSISTANT_DEFAULT_COMMANDS, AI_COMMAND_PREFIX, \
    ASSISTANT_COMMAND_EXIT
from addons.ai.src.assistant.subject.file_chat_subject import FileChatSubject
from addons.ai.src.assistant.utils.identities import AI_IDENTITY_DEFAULT
from addons.ai.src.model.ollama_model import MODEL_NAME_OLLAMA_MISTRAL
from src.helper.package import package_enable_logging
from src.helper.file import file_read, file_write
from src.helper.patch import patch_apply_in_workdir
from tests.AbstractTestCase import AbstractTestCase


class TestAiCommandTalkAsk(AbstractTestCase):
    def test_ask(self) -> None:
        assistant = Assistant(self.kernel, MODEL_NAME_OLLAMA_MISTRAL)

        self._test_ask_parsing(assistant)
        self._test_ask_formatting(assistant)
        self._test_ask_assistant(assistant)
        self._test_few_shot_prompt_template(assistant)
        self._test_few_shot_examples(assistant)
        self._test_patching(assistant)

    def _test_ask_parsing(self, assistant: Assistant) -> None:
        assistant.set_default_subject()

        for command in ASSISTANT_DEFAULT_COMMANDS:
            # Fail expected
            if command != ASSISTANT_COMMAND_EXIT:
                self._found_one_command(assistant, command, f"{command}", False)
            self._found_one_command(assistant, command, f"Lorem{command}ipsum", False)
            self._found_one_command(assistant, command, f"Lorem{command}", False)
            self._found_one_command(assistant, command, f"{command}ipsum", False)
            self._found_one_command(assistant, command, f"Lorem{AI_COMMAND_PREFIX}{command}ipsum", False)
            self._found_one_command(assistant, command, f"Lorem{AI_COMMAND_PREFIX}{command}", False)
            self._found_one_command(assistant, command, f"{AI_COMMAND_PREFIX}{command}ipsum", False)

            # Success expected
            self._found_one_command(assistant, command, f"{AI_COMMAND_PREFIX}{command}", True)
            self._found_one_command(assistant, command, f"Lorem {AI_COMMAND_PREFIX}{command}", True)
            self._found_one_command(assistant, command, f"{AI_COMMAND_PREFIX}{command} ipsum", True)
            self._found_one_command(assistant, command, f"Lorem {AI_COMMAND_PREFIX}{command} ipsum", True)

    def _found_one_command(
        self,
        assistant: Assistant,
        command: str,
        text: str,
        should_success: bool
    ):
        user_input_splits = assistant.split_user_input_commands(text)
        self.kernel.io.log(user_input_splits)
        success = any(user_input_split["command"] == command for user_input_split in user_input_splits)
        self.assertTrue(success == should_success, f"Command \"{command}\" found in text : \"{text}\"")

    def _test_ask_assistant(self, assistant: Assistant) -> None:
        assistant = Assistant(self.kernel, MODEL_NAME_OLLAMA_MISTRAL)

        self.assertGreater(len(assistant.identities.values()), 1)

        test_ext = [
            "csv",
            "html",
            "json",
            "md",
            "pdf",
        ]

        for ext in test_ext:
            sample_path = self.build_test_samples_path() + ext + "/simple." + ext

            chunks = assistant.vector_create_file_chunks(
                file_path=sample_path, file_signature=f"test-{ext}"
            )

            self.assertTrue(len(chunks) > 0)

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
        model = assistant.get_default_model()

        file_chat_subject = cast(
            FileChatSubject,
            assistant.subjects[FileChatSubject.name()]
        )

        template = model.create_few_shot_prompt_template(
            identity=assistant.identities[AI_IDENTITY_DEFAULT],
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
            ],
            input_variables_names=["file_name", "question", "source"]
        )

        self.assertTrue(
            isinstance(
                template,
                FewShotPromptTemplate
            )
        )

    def _test_few_shot_examples(self, assistant: Assistant) -> None:
        file_chat_subject = cast(
            FileChatSubject,
            assistant.subjects[FileChatSubject.name()]
        )

        base_dir = self.kernel.directory.path + 'addons/ai/samples/examples/'
        for group_name in os.listdir(base_dir):
            for example_name in os.listdir(os.path.join(base_dir, group_name)):
                example = file_chat_subject.load_example_patch(f"{group_name}/{example_name}")

                self.assertIsDict(
                    example,
                    f"Example patch \"{example_name}\" has been loaded"
                )

    def _test_patching(self, assistant: Assistant) -> None:
        target_package_json = self.kernel.directory.path + 'addons/ai/tests/resources/patches/target-package.json'
        original_package_content = file_read(target_package_json)
        patches_dir = self.kernel.directory.path + 'addons/ai/tests/resources/patches/'

        class PatchStatus(enum.Enum):
            LOAD_FAIL = 0
            LOAD_SUCCESS_APPLY_FAIL = 1
            LOAD_AND_APPLY_SUCCESS = 2

        # Mapping of patch files to their expected outcomes using the PatchStatus enum
        patch_files = {
            'package-random.patch': PatchStatus.LOAD_AND_APPLY_SUCCESS,
            'package-random-two.patch': PatchStatus.LOAD_FAIL,
            'package-random-three.patch': PatchStatus.LOAD_SUCCESS_APPLY_FAIL
        }

        for patch_file, status in patch_files.items():
            patch_path = patches_dir + patch_file
            patch_data = file_read(patch_path).encode()
            patch_set = patch.fromstring(patch_data)

            package_enable_logging()

            # Check if the patch set is loaded properly
            if not patch_set:
                if status == PatchStatus.LOAD_FAIL:
                    self.assertTrue(True, f'Patch {patch_file} expected to fail loading')
                else:
                    self.assertTrue(False, f'Patch {patch_file} unexpectedly failed to load')
            else:
                if status == PatchStatus.LOAD_AND_APPLY_SUCCESS:
                    result = patch_apply_in_workdir(patches_dir, patch_set)
                    self.assertTrue(result, f'Patch {patch_file} expected to be valid and apply successfully')
                elif status == PatchStatus.LOAD_SUCCESS_APPLY_FAIL:
                    result = patch_apply_in_workdir(patches_dir, patch_set)
                    self.assertFalse(result, f'Patch {patch_file} expected to load but fail to apply')

            # Restore the original package content after each patch test
            file_write(target_package_json, original_package_content)
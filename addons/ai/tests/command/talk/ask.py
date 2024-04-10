from addons.ai.helper.chat import TEXT_ALIGN_RIGHT, chat_format_message
from addons.ai.src.assistant.assistant import Assistant, ASSISTANT_DEFAULT_COMMANDS, AI_COMMAND_PREFIX, \
    ASSISTANT_COMMAND_EXIT
from addons.ai.src.model.ollama_model import MODEL_NAME_OLLAMA_MISTRAL
from tests.AbstractTestCase import AbstractTestCase


class TestAiCommandTalkAsk(AbstractTestCase):
    def test_ask(self) -> None:
        assistant = Assistant(self.kernel, MODEL_NAME_OLLAMA_MISTRAL)

        self._test_ask_parsing(assistant)
        self._test_ask_formatting(assistant)
        self._test_ask_assistant(assistant)

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

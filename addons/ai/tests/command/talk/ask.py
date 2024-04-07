from addons.ai.helper.chat import TEXT_ALIGN_RIGHT, chat_format_message
from addons.ai.src.assistant.assistant import Assistant
from addons.ai.src.model.ollama_model import MODEL_NAME_OLLAMA_MISTRAL
from tests.AbstractTestCase import AbstractTestCase


class TestAiCommandTalkAsk(AbstractTestCase):
    def test_ask(self) -> None:
        self._test_ask_formatting()
        self._test_ask_assistant()

    def _test_ask_assistant(self) -> None:
        assistant = Assistant(self.kernel, MODEL_NAME_OLLAMA_MISTRAL)

        self.assertGreater(len(assistant.identities.values()), 1)

        test_ext = [
            'csv',
            'html',
            'json',
            'md',
            'pdf',
        ]

        for ext in test_ext:
            sample_path = self.build_test_samples_path() + ext + '/simple.' + ext

            chunks = assistant.vector_create_file_chunks(
                file_path=sample_path,
                file_signature=f"test-{ext}"
            )

            self.assertTrue(
                len(chunks) > 0
            )

    def _test_ask_formatting(self) -> None:
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

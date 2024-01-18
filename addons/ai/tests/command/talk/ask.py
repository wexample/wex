from addons.ai.helper.chat import TEXT_ALIGN_RIGHT, chat_format_message
from tests.AbstractTestCase import AbstractTestCase


class TestAiCommandTalkAsk(AbstractTestCase):
    def test_ask(self) -> None:
        # Do not test as it is a paid / external service.
        self.assertTrue(True)

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

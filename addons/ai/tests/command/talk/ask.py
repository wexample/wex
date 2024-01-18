from addons.ai.helper.chat import chat_format_message, TEXT_ALIGN_RIGHT
from tests.AbstractTestCase import AbstractTestCase


class TestAiCommandTalkAsk(AbstractTestCase):
    def test_ask(self) -> None:
        # Do not test as it is a paid / external service.
        self.assertTrue(True)

        message = chat_format_message("Left align : Lorem ipsum dolor sit amet consecetur")
        print(message)

        message = chat_format_message("Right align : Lorem ipsum dolor sit amet consecetur", TEXT_ALIGN_RIGHT)
        print(message)

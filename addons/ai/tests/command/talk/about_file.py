from addons.ai.command.talk.about_file import ai__talk__about_file
from tests.AbstractTestCase import AbstractTestCase


class TestAiCommandTalkAboutFile(AbstractTestCase):
    def test_about_file(self) -> None:
        self.assertIsNotNone(ai__talk__about_file)

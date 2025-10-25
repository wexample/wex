from __future__ import annotations
from tests.AbstractTestCase import AbstractTestCase


class TestAiCommandTalkAboutFile(AbstractTestCase):
    def test_about_file(self) -> None:
        from addons.ai.command.talk.about_file import ai__talk__about_file
        self.assertIsNotNone(ai__talk__about_file)

from addons.ai.command.talk.about_file import ai__talk__about_file
from tests.AbstractTestCase import AbstractTestCase


class TestAiCommandTalkAboutFile(AbstractTestCase):
    def test_about_file(self) -> None:
        # TODO
        response = self.kernel.run_function(ai__talk__about_file, {
            'option': 'test'
        })

        self.assertEqual(
            response.first(),
            'something'
        )

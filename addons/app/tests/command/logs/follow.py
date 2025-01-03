from addons.app.command.logs.follow import app__logs__follow
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandLogsFollow(AbstractTestCase):
    def test_follow(self) -> None:
        # Interactive response, not tested.
        self.assertIsNotNone(
            app__logs__follow
        )

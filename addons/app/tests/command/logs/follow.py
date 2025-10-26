from __future__ import annotations

from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandLogsFollow(AbstractTestCase):
    def test_follow(self) -> None:
        from addons.app.command.logs.follow import app__logs__follow

        # Interactive response, not tested.
        self.assertIsNotNone(app__logs__follow)

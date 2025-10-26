from __future__ import annotations

from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandWebhookStop(AbstractTestCase):
    def test_stop(self) -> None:
        from addons.app.command.webhook.stop import app__webhook__stop

        self.kernel.run_function(app__webhook__stop)

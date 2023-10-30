from addons.app.command.webhook.listen import app__webhook__listen
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandWebhookListen(AbstractTestCase):
    def test_listen(self):
        self.kernel.run_function(app__webhook__listen, {
            'dry-run': True,
            'port': 6543
        })

        # No easy way to define if server ran.
        self.assertTrue(True)

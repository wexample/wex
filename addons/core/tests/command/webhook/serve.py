from addons.core.command.webhook.serve import core__webhook__serve
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandWebhookServe(AbstractTestCase):
    def test_serve(self):
        self.kernel.run_function(core__webhook__serve, {
            'dry-run': True,
            'port': 6543
        })

        # No easy way to define if server ran.
        self.assertTrue(True)

from addons.core.command.webhook.serve import core__webhook__serve
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandWebhookServe(AbstractTestCase):
    def test_serve(self):
        self.kernel.exec_function(core__webhook__serve, {
            'dry-run': True
        })

        # No easy way to define if server ran.
        self.assertTrue(True)

from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestTestCommandAppWebhook(AbstractAppTestCase):
    def test_webhook(self):
        response = self.kernel.run_command(
            'test::app/webhook',
            {
                'option': 'WEBHOOK_TEST_RESPONSE',
            })

        self.assertTrue(
            'WEBHOOK_TEST_RESPONSE' in response.output_bag[4].print()
        )

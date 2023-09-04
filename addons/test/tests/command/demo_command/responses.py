from addons.test.command.demo_command.responses import test__demo_command__responses
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponses(AbstractTestCase):
    def test_responses(self):
        response = self.kernel.run_function(
            test__demo_command__responses
        )

        self.assertEqual(
            response,
            'COLLECTION'
        )

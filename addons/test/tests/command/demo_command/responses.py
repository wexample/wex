from addons.test.command.demo_command.responses import (
    RESPONSES_DEFAULT_VALUES,
    test__demo_command__responses,
)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponses(AbstractTestCase):
    def test_responses(self):
        for type in RESPONSES_DEFAULT_VALUES:
            response = self.kernel.run_function(
                test__demo_command__responses, {"type": type}
            ).first()

            self.assertEqual(response, RESPONSES_DEFAULT_VALUES[type])

        # Python function
        response = self.kernel.run_function(
            test__demo_command__responses, {"type": "function"}
        )

        self.assertEqual(response.print(), "one")

        # Shell script
        response = self.kernel.run_function(
            test__demo_command__responses, {"type": "shell"}
        )

        self.assertTrue(
            # Word exists in "ls -la" result
            "total "
            in response.print(),
        )

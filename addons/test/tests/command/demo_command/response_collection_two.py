from addons.test.command.demo_command.response_collection_three import (
    TEST_DEMO_COMMAND_THREE_RESULT_ONE,
)
from addons.test.command.demo_command.response_collection_two import (
    TEST_DEMO_COMMAND_TWO_RESULT_FIRST,
    TEST_DEMO_COMMAND_TWO_RESULT_SHELL,
    test__demo_command__response_collection_two,
)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponseCollectionTwo(AbstractTestCase):
    def test_response_collection_two(self) -> None:
        result = self.kernel.run_function(test__demo_command__response_collection_two)

        self.assertEqual(result.first(), TEST_DEMO_COMMAND_TWO_RESULT_FIRST)

        self.assertEqual(
            result.output_bag[1].first(), TEST_DEMO_COMMAND_TWO_RESULT_FIRST + "(2)"
        )

        self.assertEqual(
            result.output_bag[3].first(), TEST_DEMO_COMMAND_TWO_RESULT_SHELL
        )

        self.assertEqual(
            result.output_bag[7].first(), TEST_DEMO_COMMAND_THREE_RESULT_ONE
        )

        self.assertEqual(result.output_bag[8].first(), "....THREE:shell-response")

        self.assertEqual(
            result.output_bag[9].first(),
            "..TWO:interactive-shell-response",
        )

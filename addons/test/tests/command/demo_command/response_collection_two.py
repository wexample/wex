from addons.test.command.demo_command.response_collection_three import \
    TEST_DEMO_COMMAND_THREE_RESULT_ONE
from addons.test.command.demo_command.response_collection_two import (
    TEST_DEMO_COMMAND_TWO_RESULT_FIRST,
    test__demo_command__response_collection_two)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponseCollectionTwo(AbstractTestCase):
    def test_response_collection_two(self) -> None:
        result = self.kernel.run_function(test__demo_command__response_collection_two)

        self.assertEqual(result.first(), TEST_DEMO_COMMAND_TWO_RESULT_FIRST)

        self.assertEqual(
            result.get(1).first(), TEST_DEMO_COMMAND_TWO_RESULT_FIRST + "(2)"
        )

        # This is interactive
        self.assertEqual(
            result.get(3).first(),
            # TEST_DEMO_COMMAND_TWO_RESULT_SHELL
            "",
        )

        self.assertEqual(result.get(7).first(), TEST_DEMO_COMMAND_THREE_RESULT_ONE)

        # This is interactive
        self.assertEqual(
            result.get(8).first(),
            # "....THREE:shell-response"
            "",
        )

        # This is interactive
        self.assertEqual(
            result.get(9).first(),
            # "..TWO:interactive-shell-response"
            "",
        )

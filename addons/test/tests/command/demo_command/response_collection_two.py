from addons.test.command.demo_command.response_collection_two import test__demo_command__response_collection_two, \
    TEST_DEMO_COMMAND_TWO_RESULT_FIRST, TEST_DEMO_COMMAND_TWO_RESULT_SHELL
from addons.test.command.demo_command.response_collection_three import TEST_DEMO_COMMAND_THREE_RESULT_ONE
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponseCollectionTwo(AbstractTestCase):
    def test_response_collection_two(self):
        result = self.kernel.run_function(test__demo_command__response_collection_two)

        self.assertEqual(
            result.first(),
            TEST_DEMO_COMMAND_TWO_RESULT_FIRST
        )

        self.assertEqual(
            result.output_bag[1].first(),
            TEST_DEMO_COMMAND_TWO_RESULT_FIRST + '(2)'
        )

        self.assertEqual(
            result.output_bag[3].first(),
            TEST_DEMO_COMMAND_TWO_RESULT_SHELL
        )

        self.assertEqual(
            result.output_bag[5].first(),
            TEST_DEMO_COMMAND_THREE_RESULT_ONE
        )

        self.assertEqual(
            result.output_bag[6].first(),
            '....THREE:shell-response'
        )

        self.assertEqual(
            result.output_bag[8],
            '..TWO:interactive-shell-response',
        )

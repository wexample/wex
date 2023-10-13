from addons.test.command.demo_command.response_collection_three import test__demo_command__response_collection_three, \
    TEST_DEMO_COMMAND_THREE_RESULT_ONE, TEST_DEMO_COMMAND_THREE_RESULT_SHELL, TEST_DEMO_COMMAND_THREE_RESULT_FUNCTION
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponseCollectionThree(AbstractTestCase):
    def test_response_collection_three(self):
        result = self.kernel.run_function(test__demo_command__response_collection_three)

        self.assertEqual(
            result.first(),
            TEST_DEMO_COMMAND_THREE_RESULT_FUNCTION
        )

        self.assertEqual(
            result.output_bag[1].first(),
            TEST_DEMO_COMMAND_THREE_RESULT_ONE
        )

        self.assertEqual(
            result.output_bag[2].first(),
            TEST_DEMO_COMMAND_THREE_RESULT_SHELL
        )

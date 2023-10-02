from addons.test.command.demo_command.response_collection_two import test__demo_command__response_collection_two, \
    TEST_DEMO_COMMAND_TWO_RESULT_ONE, TEST_DEMO_COMMAND_TWO_RESULT_SHELL, TEST_DEMO_COMMAND_TWO_RESULT_FUNCTION
from addons.test.command.demo_command.response_collection_three import TEST_DEMO_COMMAND_THREE_RESULT_ONE
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponseCollectionTwo(AbstractTestCase):
    def test_response_collection_two(self):
        result = self.kernel.run_function(test__demo_command__response_collection_two)

        self.assertEqual(
            result.output_bag[0].output_bag[0],
            TEST_DEMO_COMMAND_TWO_RESULT_ONE
        )

        self.assertEqual(
            result.output_bag[1].output_bag[0].split(':')[1].strip(),
            TEST_DEMO_COMMAND_TWO_RESULT_ONE
        )

        self.assertEqual(
            result.output_bag[4].output_bag[0],
            TEST_DEMO_COMMAND_TWO_RESULT_SHELL
        )

        self.assertEqual(
            result.output_bag[6].output_bag[0],
            TEST_DEMO_COMMAND_THREE_RESULT_ONE
        )

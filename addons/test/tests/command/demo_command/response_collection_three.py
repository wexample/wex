from addons.test.command.demo_command.response_collection_three import (
    TEST_DEMO_COMMAND_THREE_RESULT_FUNCTION,
    TEST_DEMO_COMMAND_THREE_RESULT_ONE,
    TEST_DEMO_COMMAND_THREE_RESULT_SHELL,
    test__demo_command__response_collection_three,
)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponseCollectionThree(AbstractTestCase):
    def test_response_collection_three(self) -> None:
        result = self.kernel.run_function(test__demo_command__response_collection_three)

        self.assertEqual(result.first(), TEST_DEMO_COMMAND_THREE_RESULT_FUNCTION)

        self.assertEqual(result.get(1).first(), TEST_DEMO_COMMAND_THREE_RESULT_ONE)

        self.assertEqual(result.get(2).first(), TEST_DEMO_COMMAND_THREE_RESULT_SHELL)

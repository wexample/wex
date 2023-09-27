from addons.test.command.demo_command.response_collection import test__demo_command__response_collection, \
    TEST_DEMO_COMMAND_RESULT_ONE
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponseCollection(AbstractTestCase):
    def test_response_collection(self):
        response = self.kernel.run_function(
            test__demo_command__response_collection
        )

        self.assertEqual(
            response[0],
            'free-text'
        )

        self.assertEqual(
            response[3],
            TEST_DEMO_COMMAND_RESULT_ONE,
            'First function works'
        )

        self.assertEqual(
            response[4]['old'],
            TEST_DEMO_COMMAND_RESULT_ONE,
            'Second function received first function result'
        )

        self.assertEqual(
            response[5]['type'],
            type({}),
            'Third function receive a previous value of type "dict"'
        )

        self.assertIn(
            'README.md',
            response[6],
            'The ls -la, which might have been executed at app root, should display some basic files'
        )

        self.assertEqual(
            response[9],
            TEST_DEMO_COMMAND_RESULT_ONE,
            'The first callback has been called in a second level collection'
        )

        self.assertEqual(
            response[10],
            response[11]['ls'],
            'The result of subprocess has been sent to next callback'
        )


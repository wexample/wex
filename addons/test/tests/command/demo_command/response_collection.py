import subprocess

from addons.test.command.demo_command.response_collection import test__demo_command__response_collection, \
    TEST_DEMO_COMMAND_RESULT_ONE
from src.helper.command import core_call_to_shell_command
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponseCollection(AbstractTestCase):
    def test_response_collection(self):
        response = self.kernel.run_function(
            test__demo_command__response_collection
        )

        self.assertEqual(
            response.output_bag[0].output_bag[0],
            'free-text'
        )

        self.assertEqual(
            response.output_bag[3].output_bag[0],
            TEST_DEMO_COMMAND_RESULT_ONE,
            'First function works'
        )

        self.assertEqual(
            response.output_bag[4].output_bag[0]['old'],
            TEST_DEMO_COMMAND_RESULT_ONE,
            'Second function received first function result'
        )

        self.assertEqual(
            response.output_bag[5].output_bag[0]['type'],
            type({}),
            'Third function receive a previous value of type "dict"'
        )

        self.assertIn(
            'README.md',
            response.output_bag[6].output_bag[0],
            'NonInteractiveShellCommandResponse: '
            'The ls -la, which might have been executed at app root, should display some basic files'
        )

        self.assertEqual(
            response.output_bag[13].output_bag[0],
            TEST_DEMO_COMMAND_RESULT_ONE,
            'callback function : '
            'The first callback has been called in a second level collection'
        )

        self.assertEqual(
            response.output_bag[14].output_bag[0],
            response.output_bag[15].output_bag[0]['passed'],
            'The result of subprocess has been sent to next callback'
        )

        # Execute in standard mode in a subshell.
        # Can take few seconds.
        self.kernel.io.log('Running collection test in standard mode...')
        standard_mode_response = (
            (subprocess
             .run(core_call_to_shell_command(
                self.kernel,
                test__demo_command__response_collection
            ),
                capture_output=True)
             .stdout.
             decode('utf-8').strip()))

        # Compare outputs.
        self.assertMultiLineEqual(
            response.print(),
            standard_mode_response,
            'Both standard and fat mode commands should return the exact same data'
        )

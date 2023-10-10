import subprocess

from addons.test.command.demo_command.response_collection import test__demo_command__response_collection, \
    TEST_DEMO_COMMAND_RESULT_FIRST_FUNCTION
from src.helper.command import core_call_to_shell_command
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponseCollection(AbstractTestCase):
    def test_response_collection(self):
        response = self.kernel.run_function(
            test__demo_command__response_collection
        )

        self.assertEqual(
            response.first(),
            'simple-response-text'
        )

        self.assertEqual(
            response.output_bag[6].first(),
            TEST_DEMO_COMMAND_RESULT_FIRST_FUNCTION,
            'First function works'
        )

        self.assertEqual(
            response.output_bag[7].first()['old'],
            TEST_DEMO_COMMAND_RESULT_FIRST_FUNCTION,
            'Second function received first function result'
        )

        self.assertEqual(
            response.output_bag[8].first()['type'],
            type({}),
            'Third function receive a previous value of type "dict"'
        )

        found_readme = False
        for line in response.output_bag[9].first():
            if 'README.md' in line:
                found_readme = True
                break

        self.assertTrue(
            found_readme,
            'NonInteractiveShellCommandResponse: '
            'The ls -la, which might have been executed at app root, should display some basic files'
        )

        self.assertEqual(
            response.output_bag[15].first(),
            TEST_DEMO_COMMAND_RESULT_FIRST_FUNCTION,
            'callback function : '
            'The first callback has been called in a second level collection'
        )

        self.assertEqual(
            response.output_bag[16].first(),
            response.output_bag[17].first()['passed'],
            'The result of subprocess has been sent to next callback'
        )

        # Execute in standard mode in a subshell.
        # Can take few seconds.
        self.kernel.io.log('Running collection test in standard mode...')
        current_verbosity = self.kernel.verbosity
        self.kernel.verbosity = 0

        standard_mode_response = (
            (subprocess
             .run(core_call_to_shell_command(
                self.kernel,
                test__demo_command__response_collection
            ),
                capture_output=True)
             .stdout
             .decode('utf-8')
             .strip()))
        self.kernel.verbosity = current_verbosity

        self.write_test_result(
            'response_collection_a',
            'FAST_MODE\n'
            +response.print()
        )

        self.write_test_result(
            'response_collection_b',
            'STANDARD_MODE\n'
            +standard_mode_response
        )

        # Compare outputs.
        self.assertMultiLineEqual(
            response.print(),
            standard_mode_response,
            'Both standard and fat mode commands should return the exact same data'
        )

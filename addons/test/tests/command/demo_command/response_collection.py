import os
import subprocess

from addons.test.command.demo_command.response_collection import (
    test__demo_command__response_collection,
)
from src.core.response.queue_collection.QueuedCollectionStopResponse import (
    QueuedCollectionStopResponse,
)
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.helper.command import internal_command_to_shell
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponseCollection(AbstractTestCase):
    def assertCollectionOutputListItemsMatch(
        self, response, all_expected, start_at: int = 0
    ):
        count = start_at

        for expected in all_expected:
            self.assertEqual(expected, response.output_bag[count].output_bag[0])

            count += 1

    def test_response_collection(self):
        response = self.kernel.run_function(test__demo_command__response_collection)

        first_response_print = response.print()

        # Write result in a file
        self.write_test_result(
            "response_collection_a", "FAST_MODE" + os.linesep + first_response_print
        )

        self.assertEqual(response.first(), "simple-response-text")

        self.assertTrue(
            isinstance(response.output_bag[14], QueuedCollectionResponse),
            "This item should be a collection of responses, returned by a function",
        )

        self.assertEqual(
            response.output_bag[15].print(),
            "--sub-collection-direct:simple-text",
            "The item just after the collection is the rendered content as output bags are merged in fast mode",
        )

        response = self.kernel.run_function(
            test__demo_command__response_collection, {"abort": True}
        )

        self.assertTrue(
            isinstance(
                response.output_bag[-1].output_bag[-1].output_bag[-1],
                QueuedCollectionStopResponse,
            )
        )

        # Execute in standard mode in a subshell.
        # Can take few seconds.
        self.log("Running collection test in standard mode...")
        current_verbosity = self.kernel.verbosity
        self.kernel.verbosity = 0

        internal_command = self.kernel.get_command_resolver(
            test__demo_command__response_collection.function.callback.command_type
        ).build_command_from_function(test__demo_command__response_collection)

        standard_mode_response = (
            subprocess.run(
                internal_command_to_shell(
                    kernel=self.kernel, internal_command=internal_command
                ),
                capture_output=True,
            )
            .stdout.decode("utf-8")
            .strip()
        )
        self.kernel.verbosity = current_verbosity

        self.write_test_result(
            "response_collection_b",
            "STANDARD_MODE" + os.linesep + standard_mode_response,
        )

        # Compare outputs.
        self.assertMultiLineEqual(
            first_response_print,
            standard_mode_response,
            "Both standard and fast mode commands should return the exact same data",
        )

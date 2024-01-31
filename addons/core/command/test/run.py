import os
import sys
import unittest
from typing import TYPE_CHECKING, Any, Optional, cast

from addons.core.command.test.cleanup import core__test__cleanup
from src.const.globals import COMMAND_TYPE_ADDON
from src.const.types import StringsList
from src.core.response.InteractiveShellCommandResponse import (
    InteractiveShellCommandResponse,
)
from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager import (
    AbstractQueuedCollectionResponseQueueManager,
)
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.decorator.alias import alias
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option
from src.helper.module import module_load_from_file

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@alias("test")
@as_sudo()
@command(help="Run all tests or given command test")
@option("--command", "-c", type=str, required=False, help="Single command to test")
def core__test__run(
    kernel: "Kernel", command: Optional[str] = None
) -> QueuedCollectionResponse:
    def _remote_command(command_part: StringsList):
        return InteractiveShellCommandResponse(
            kernel,
            [
                "docker",
                "compose",
                "-f",
                ".wex/docker/docker-compose.test-remote.yml",
            ]
            + command_part,
        )

    def _start_remote(queue: AbstractQueuedCollectionResponseQueueManager):
        return _remote_command(
            [
                "up",
                "-d",
            ]
        )

    def _stop_remote(queue: AbstractQueuedCollectionResponseQueueManager):
        return _remote_command(
            [
                "down",
            ]
        )

    def _run_tests(queue: AbstractQueuedCollectionResponseQueueManager):
        kernel.run_function(core__test__cleanup)

        kernel.io.log("Starting test suite..")

        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        os.chdir(kernel.directory.path)

        if not command:
            suite.addTests(
                loader.discover(os.path.join(kernel.directory.path, "tests"))
            )

        kernel.io.log("Starting addons tests suites..")

        for addon_data in (
            kernel.get_command_resolver(COMMAND_TYPE_ADDON).get_registry_data().values()
        ):
            for command_name, command_data in addon_data["commands"].items():
                if (
                    "test" in command_data
                    and command_data["test"]
                    and (
                        (not command)
                        or command_name == command
                        or (
                            command.endswith("*")
                            and command_name.startswith(command[:-1])
                        )
                    )
                ):
                    kernel.io.log(f"Found test for command: {command_name}")

                    module = module_load_from_file(
                        command_data["test"], f"{command_name}_test"
                    )

                    suite.addTests(loader.loadTestsFromModule(cast(Any, module)))

        result = unittest.TextTestRunner(failfast=True).run(suite)

        if not result.wasSuccessful():
            sys.exit(1)

        kernel.run_function(core__test__cleanup)

    remote_address = "TEST_REMOTE_ADDRESS" in os.environ
    if not remote_address:
        steps = [
            _run_tests,
        ]
    else:
        steps = [
            _start_remote,
            _run_tests,
            _stop_remote,
        ]

    return QueuedCollectionResponse(
        kernel,
        steps,
    )

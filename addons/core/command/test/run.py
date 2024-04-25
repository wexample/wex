import os
import sys
import time
import unittest
from typing import TYPE_CHECKING, Any, Optional, cast

from addons.app.command.env.get import _app__env__get
from addons.core.command.test.cleanup import core__test__cleanup
from src.const.globals import COMMAND_TYPE_ADDON
from src.const.types import StringsList
from src.core.response.InteractiveShellCommandResponse import (
    InteractiveShellCommandResponse,
)
from src.core.response.QueuedCollectionResponse import (
    QueuedCollectionResponse,
    QueuedCollectionResponseCollection,
)
from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager import (
    AbstractQueuedCollectionResponseQueueManager,
)
from src.decorator.alias import alias
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option
from src.helper.command import execute_command_sync
from src.helper.module import module_load_from_file

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@alias("test")
@as_sudo()
@command(help="Run all tests or given command test")
@option("--command", "-c", type=str, required=False, help="Single command to test")
@option(
    "--debug",
    "-d",
    type=bool,
    is_flag=True,
    default=False,
    required=False,
    help="Single command to test",
)
def core__test__run(
    kernel: "Kernel", command: Optional[str] = None, debug: bool = False
) -> QueuedCollectionResponse:
    def _remote_compose(command_part: StringsList) -> InteractiveShellCommandResponse:
        test_env = _app__env__get(
            kernel, kernel.directory.path, key="TEST_REMOTE_ENV", default="pipeline"
        )

        suffix = "." + test_env if test_env != "pipeline" else ""

        return InteractiveShellCommandResponse(
            kernel,
            [
                "docker",
                "compose",
                "-f",
                f"{kernel.directory.path}.wex/docker/test_remote/docker-compose.test-remote{suffix}.yml",
            ]
            + command_part,
            workdir=kernel.directory.path,
        )

    def _start_remote(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> InteractiveShellCommandResponse:
        return _remote_compose(
            [
                "up",
                "-d",
            ]
        )

    def _wait_remote(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> None:
        success = False
        while not success:
            success, content = execute_command_sync(
                kernel,
                [
                    "docker",
                    "exec",
                    "wex_test_remote",
                    "test",
                    "-f",
                    "/test_remote.ready",
                ],
                ignore_error=True,
            )
            kernel.io.log("Test remote server starting...")
            time.sleep(10)

    def _stop_remote(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> InteractiveShellCommandResponse:
        return _remote_compose(
            [
                "down",
            ]
        )

    def _cleanup(queue: AbstractQueuedCollectionResponseQueueManager) -> None:
        kernel.run_function(core__test__cleanup)

    def _run_tests(queue: AbstractQueuedCollectionResponseQueueManager) -> None:
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

    steps: QueuedCollectionResponseCollection

    # Debug focus on speed.
    if debug:
        steps = [_run_tests]
    else:
        steps = [
            _stop_remote,
            _start_remote,
            _wait_remote,
            _run_tests,
            _cleanup,
            _stop_remote,
        ]

    return QueuedCollectionResponse(
        kernel,
        steps,
    )

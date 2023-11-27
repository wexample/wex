import importlib.util
import os
import sys
import unittest
from typing import TYPE_CHECKING, Optional

from addons.app.const.app import APP_ENV_LOCAL
from addons.core.command.core.cleanup import core__core__cleanup
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.alias import alias
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option
from src.helper.command import execute_command_tree

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@alias("test")
@as_sudo()
@command(help="Run all tests or given command test")
@option("--command", "-c", type=str, required=False, help="Single command to test")
def core__test__run(kernel: "Kernel", command: Optional[str] = None):
    # In local env, script are started manually,
    # then we remove every docker container to ensure no
    if kernel.registry_structure.content["env"] == APP_ENV_LOCAL:
        execute_command_tree(
            kernel,
            [
                "docker",
                "rm",
                "-f",
                ["docker", "ps", "-q", "--filter", "name=test_app_"],
            ],
            ignore_error=True,
        )

    # Remove all temp files.
    kernel.run_function(function=core__core__cleanup, args={"test": True})

    kernel.io.log("Starting test suite..")

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    os.chdir(kernel.get_path("root"))

    if not command:
        suite.addTests(loader.discover(os.path.join(kernel.get_path("root"), "tests")))

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
                    or (command.endswith("*") and command_name.startswith(command[:-1]))
                )
            ):
                kernel.io.log(f"Found test for command: {command_name}")

                spec = importlib.util.spec_from_file_location(
                    f"{command_name}_test", command_data["test"]
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                suite.addTests(loader.loadTestsFromModule(module))

    result = unittest.TextTestRunner(failfast=True).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

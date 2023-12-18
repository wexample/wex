from src.helper.command import execute_command_tree_sync
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command
from typing import TYPE_CHECKING
from addons.core.command.core.cleanup import core__core__cleanup

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Description", command_type=COMMAND_TYPE_ADDON)
def core__test__cleanup(kernel: "Kernel") -> None:
    kernel.io.log("Cleaning up tests...")

    # In local env, script are started manually,
    # then we remove every docker container to ensure no
    execute_command_tree_sync(
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

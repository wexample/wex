from typing import TYPE_CHECKING

from addons.core.command.core.cleanup import core__core__cleanup
from addons.app.helper.docker import docker_remove_filtered_container
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.command import command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Description", command_type=COMMAND_TYPE_ADDON)
def core__test__cleanup(kernel: "Kernel") -> None:
    kernel.io.log("Cleaning up tests...")

    docker_remove_filtered_container(kernel, "test_app_")

    # Remove all temp files.
    kernel.run_function(function=core__core__cleanup, args={"test": True})

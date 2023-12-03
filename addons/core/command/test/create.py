from typing import TYPE_CHECKING, Optional

from src.const.globals import COMMAND_TYPE_ADDON
from src.const.types import StringsList
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option
from src.helper.test import create_test_from_command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@as_sudo()
@command(help="Create a test file for command")
@option(
    "--all",
    "-a",
    type=str,
    is_flag=True,
    required=False,
    help="Create all missing tests",
)
@option("--command", "-c", type=str, required=False, help="Command name")
@option(
    "--force",
    "-f",
    type=bool,
    required=False,
    is_flag=True,
    default=False,
    help="Force to create file if exists",
)
def core__test__create(
    kernel: "Kernel",
    command: Optional[str] = None,
    all: bool = False,
    force: bool = False,
) -> Optional[str | StringsList]:
    if not command:
        if all:
            output: StringsList = []
            # Create all missing tests
            for command_found, command_data in (
                kernel.resolvers[COMMAND_TYPE_ADDON].get_commands_registry().items()
            ):
                command_built = create_test_from_command(kernel, command_found, force)
                assert isinstance(command_built, str)

                output.append(command_built)
            return output
        return None
    else:
        return create_test_from_command(kernel, command, force)

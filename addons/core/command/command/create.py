import os
from typing import TYPE_CHECKING

from addons.core.command.test.create import core__test__create
from src.const.globals import (
    COMMAND_CHAR_USER,
    COMMAND_EXTENSION_PYTHON,
    COMMAND_TYPE_ADDON,
    COMMAND_TYPE_CORE,
)
from src.const.types import StringKeysDict
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option
from src.helper.file import file_create_from_template

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@as_sudo()
@command(help="Create a new command and test files")
@option(
    "--command",
    "-c",
    type=str,
    required=True,
    help="Full name of the command, i.e. addon::some/thing",
)
@option(
    "--force",
    "-f",
    type=bool,
    required=False,
    is_flag=True,
    default=False,
    help="Force to create file if exists",
)
@option(
    "--extension",
    "-e",
    type=str,
    required=False,
    default=COMMAND_EXTENSION_PYTHON,
    help="Script file extension and resulting format",
)
def core__command__create(
    kernel: "Kernel",
    command: str,
    force: bool = False,
    extension: str = COMMAND_EXTENSION_PYTHON,
) -> StringKeysDict:
    kernel.io.log("Creating command file...")
    request = kernel.create_command_request(command)

    if not request:
        kernel.io.message(f"Unable to process command : {command}")
        return

    command_path: str = request.resolver.build_path_or_fail(
        request=request, extension=extension
    )

    # File exists
    if not os.path.exists(command_path) or force:
        command_type = request.resolver.get_type()

        if command_type == COMMAND_TYPE_CORE:
            kernel.io.message(f"Unable to create core command : {command}")
            return
        # User wants to create some/command, but with no addons name
        # So we suggest user want to create a local user command.
        elif command_type == COMMAND_TYPE_ADDON:
            if not command_path:
                kernel.io.log("No given addon name, creating a local user command...")

                return kernel.run_function(
                    core__command__create, {"command": f"{COMMAND_CHAR_USER}{command}"}
                ).first()

        os.makedirs(os.path.dirname(command_path), exist_ok=True)

        function_name = request.resolver.get_function_name(list(request.match.groups()))

        file_create_from_template(
            f'{kernel.get_path("templates")}command.{extension}.tpl',
            command_path,
            {
                "function_name": function_name,
                "command_type": command_type.upper(),
                "command_type_constant": f"COMMAND_TYPE_{command_type.upper()}",
            },
        )

        kernel.io.message(f"Created command file : {command_path}")

    test_file = kernel.run_function(core__test__create, {"command": command}).first()

    kernel.io.log("Giving files permission...")
    request.resolver.set_command_file_permission(command_path)
    request.resolver.set_command_file_permission(test_file)

    return {"command": command_path, "test": test_file}

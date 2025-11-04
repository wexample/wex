from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any, NoReturn, cast

from src.const.types import ShellCommandResponseTuple

if TYPE_CHECKING:
    from subprocess import Popen

    from src.const.types import ShellCommandsDeepList, ShellCommandsList
    from src.core.command.ScriptCommand import ScriptCommand
    from src.utils.kernel import Kernel


def apply_command_decorator(
    kernel: Kernel,
    function: ScriptCommand,
    group: str,
    name: str,
    options: dict[str, str] | None = None,
) -> NoReturn | ScriptCommand:
    from src.core.command.ScriptCommand import ScriptCommand

    if group in kernel.decorators and name in kernel.decorators[group]:
        decorator = kernel.decorators[group][name]
        options = options or {}

        script_command = decorator(**options)(function)
        assert isinstance(script_command, ScriptCommand)

        return script_command
    else:
        kernel.io.error(f"Missing decorator {group}.{name}")


def command_escape(string: str, quote_char: str = '"') -> str:
    # Escape existing quotes
    escaped_string = string.replace("\\", "\\\\").replace(quote_char, "\\" + quote_char)
    # Add quotes around the escaped string
    return quote_char + escaped_string + quote_char


def command_exists(shell_command: str) -> bool:
    from subprocess import Popen

    process = Popen(
        "command -v " + shell_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out_content, err_content = process.communicate()

    return out_content.decode() != ""


def command_get_option(
    script_command: ScriptCommand, option_name: str
) -> click.core.Option | None:
    for option in script_command.click_command.params:
        if option.name == option_name:
            return cast(click.core.Option, option)

    return None


def command_to_string(command: ShellCommandsList | ShellCommandsDeepList | str) -> str:
    if isinstance(command, str):
        return command

    output = []

    for item in command:
        if isinstance(item, list):
            output.append("$(" + command_to_string(item) + ")")
        else:
            output.append(item)

    return " ".join(output)


def execute_command_async(
    kernel: Kernel,
    command: ShellCommandsList,
    working_directory: str | None = None,
    **kwargs: Any,
) -> Popen[Any]:
    from subprocess import Popen

    from src.const.globals import VERBOSITY_LEVEL_MAXIMUM
    from src.helper.file import file_create_parent_dir

    if working_directory is None:
        working_directory = os.getcwd()

    command_str = command_to_string(command)
    kernel.io.log(
        f"Running shell command : {command_str}", verbosity=VERBOSITY_LEVEL_MAXIMUM
    )

    tmp_dir = os.path.join(kernel.get_or_create_path("tmp"), "subprocess") + os.sep

    task_id = kernel.get_task_id()
    popen_args = {
        "cwd": working_directory,
        "start_new_session": True,
        "stdout": open(file_create_parent_dir(tmp_dir + task_id + ".stdout"), "a"),
        "stderr": open(file_create_parent_dir(tmp_dir + task_id + ".stderr"), "a"),
        **kwargs,
    }

    return Popen(
        command,
        **popen_args,
    )


def execute_command_sync(
    kernel: Kernel,
    command: ShellCommandsList | str,
    cwd: str | None = None,
    ignore_error: bool = False,
    interactive: bool = False,
    as_sudo_user: bool = True,
    **kwargs: Any,
) -> ShellCommandResponseTuple:
    from subprocess import Popen

    from src.const.globals import VERBOSITY_LEVEL_MAXIMUM
    from src.helper.user import get_user_or_sudo_user

    if cwd is None:
        cwd = os.getcwd()

    if isinstance(command, str):
        command = command.split()

    if as_sudo_user:
        command_prefix: list[str] = ["sudo", "-u", get_user_or_sudo_user()]
        if isinstance(command, str):
            cmd_list: list[str] = command.split()
        else:
            cmd_list = list(command)
        command = command_prefix + cmd_list

    command_str = command_to_string(command)

    kernel.io.log(
        f"Running shell command: {command_str}", verbosity=VERBOSITY_LEVEL_MAXIMUM
    )

    try:
        if interactive:
            process = Popen(
                command,
                cwd=Path(cwd),
                stdin=None,
                stdout=None,
                stderr=None,
                **kwargs,
            )
            process.wait()
        else:
            process = Popen(
                command,
                cwd=Path(cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                **kwargs,
            )

        output, errors = process.communicate()

        output_lines = output.splitlines() if output else []
        error_lines = errors.splitlines() if errors else []

        if process.returncode != 0 and not ignore_error:
            kernel.io.error(
                f"Command response code error: {command_str}\n\nStdout:\n{os.linesep.join(output_lines)}\n\nStderr:\n{os.linesep.join(error_lines)}"
            )
            return False, error_lines

        kernel.io.log("\n".join(output_lines), verbosity=VERBOSITY_LEVEL_MAXIMUM)
        return process.returncode == 0, output_lines

    except subprocess.CalledProcessError as e:
        kernel.io.error(f"Error when running command: {command_str}\n\n{str(e)}")
        return False, e.stderr.splitlines() if e.stderr else []


def execute_command_tree_sync(
    kernel: Kernel,
    command_tree: ShellCommandsDeepList,
    working_directory: str | None = None,
    ignore_error: bool = False,
    interactive: bool = False,
    as_sudo_user: bool = True,
    **kwargs: Any,
) -> ShellCommandResponseTuple:
    from subprocess import Popen

    from src.const.types import ShellCommandsDeepList, ShellCommandsList

    if isinstance(command_tree, list) and any(
        isinstance(i, list) for i in command_tree
    ):
        # If the command_tree is a list and contains sub lists (nested commands)
        # We execute the innermost command first
        for i, sub_command in enumerate(command_tree):
            if isinstance(sub_command, list):
                # Recursive call to execute the nested command
                result = execute_command_tree_sync(
                    kernel=kernel,
                    command_tree=cast(ShellCommandsDeepList, sub_command),
                    working_directory=working_directory,
                    ignore_error=ignore_error,
                    as_sudo_user=as_sudo_user,
                    **kwargs,
                )

                if not isinstance(result, Popen):
                    success, output = result

                    if not success:
                        return success, output

                    # Replace the nested command with the output of its execution
                    command_tree[i : i + 1] = output

                # Now command_tree is a flat list with the results of the inner command included

    # Execute the modified (flattened) command_tree with the results of inner commands
    return execute_command_sync(
        kernel=kernel,
        command=cast(ShellCommandsList, command_tree),
        cwd=working_directory,
        ignore_error=ignore_error,
        interactive=interactive,
        as_sudo_user=as_sudo_user,
        **kwargs,
    )


def internal_command_to_shell(
    kernel: Kernel, internal_command: str, args: None | list[str] = None
) -> ShellCommandsList:
    from src.const.globals import (
        VERBOSITY_LEVEL_MAXIMUM,
        VERBOSITY_LEVEL_MEDIUM,
        VERBOSITY_LEVEL_QUIET,
    )
    from src.core.IOManager import IO_DEFAULT_LOG_LENGTH

    command = (
        ["bash", kernel.get_path("core.cli"), internal_command]
        + (args or [])
        + ["--kernel-task-id", kernel.get_task_id()]
    )

    if kernel.verbosity == VERBOSITY_LEVEL_QUIET:
        command += ["--quiet"]
    elif kernel.verbosity == VERBOSITY_LEVEL_MEDIUM:
        command += ["--vv"]
    elif kernel.verbosity == VERBOSITY_LEVEL_MAXIMUM:
        command += ["--vvv"]

    if kernel.io.log_length != IO_DEFAULT_LOG_LENGTH:
        command += ["--log-length", str(kernel.io.log_length)]

    return command


def is_same_command(command_a: ScriptCommand, command_b: ScriptCommand) -> bool:
    if (
        command_a.click_command.callback is not None
        and command_b.click_command.callback is not None
    ):
        return (
            command_a.click_command.callback.__name__
            == command_b.click_command.callback.__name__
        )
    return False

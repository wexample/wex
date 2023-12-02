from __future__ import annotations

import os
import signal
from typing import TYPE_CHECKING, List, Optional, cast

import psutil

from src.const.globals import VERBOSITY_LEVEL_MAXIMUM
from src.const.types import ShellCommandsDeepList
from src.helper.command import (
    command_to_string,
    execute_command_sync,
    internal_command_to_shell,
)

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def process_post_exec(kernel: "Kernel", command: ShellCommandsDeepList | str) -> None:
    # All command should be executed by default in the same current workdir.
    if isinstance(command, list):
        kernel.post_exec.append(cast(ShellCommandsDeepList, ["cd", os.getcwd(), "&&"] + command))
    else:
        kernel.post_exec.append(f"cd {os.getcwd()} && " + command)

    kernel.io.log(
        "Queuing shell command : " + command_to_string(command),
        verbosity=VERBOSITY_LEVEL_MAXIMUM,
    )

def process_post_exec_function(
    kernel: "Kernel",
    internal_command: str,
    args: Optional[List[str]] = None,
    is_async: bool = False,
) -> None:
    command = internal_command_to_shell(
        kernel=kernel, internal_command=internal_command, args=args
    )

    if is_async:
        command.insert(0, "nohup")
        command += [">", "/dev/null", "2>&1", "&"]

    process_post_exec(kernel, cast(ShellCommandsDeepList, command))


def process_kill_by_command(kernel: "Kernel", command: str) -> None:
    success, pids = execute_command_sync(
        kernel, ["pgrep", "-f", command], ignore_error=True
    )

    if pids:
        for pid in pids:
            kernel.io.log(f"Killing process {pid}")
            os.kill(int(pid), signal.SIGTERM)


def process_kill(process: psutil.Process) -> bool:
    try:
        process.terminate()
        return True
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return False


def process_kill_by_port(port: int) -> bool:
    process = process_get_all_by_port(port)

    if process is None:
        return False

    process_kill(process)

    return True


def process_get_all_by_port(port: int) -> Optional[psutil.Process]:
    port = int(port)

    for process in psutil.process_iter():
        try:
            connections = process.connections()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
        for connection in connections:
            if connection.laddr.port == port:
                return process
    return None

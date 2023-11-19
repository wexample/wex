from __future__ import annotations
import os
from src.core import Kernel
from src.helper.command import command_to_string, internal_command_to_shell
from src.const.globals import VERBOSITY_LEVEL_MAXIMUM
from typing import List, Optional


def process_post_exec(
        kernel: Kernel,
        command: List[str]) -> None:
    # All command should be executed by default in the same current workdir.
    if isinstance(command, list):
        command = ['cd', os.getcwd(), '&&'] + command
    else:
        command = f'cd {os.getcwd()} && ' + command

    kernel.io.log(
        'Queuing shell command : ' + command_to_string(command),
        verbosity=VERBOSITY_LEVEL_MAXIMUM
    )
    kernel.post_exec.append(command)


def process_post_exec_function(
        kernel: Kernel,
        internal_command: str,
        args: Optional[List[str]] = None,
        is_async: bool = False) -> None:
    command = internal_command_to_shell(
        kernel=kernel,
        internal_command=internal_command,
        args=args
    )

    if is_async:
        command.insert(0, 'nohup')
        command += ['>', '/dev/null', '2>&1', '&']

    process_post_exec(
        kernel,
        command
    )

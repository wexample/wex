from __future__ import annotations

import re
from typing import TYPE_CHECKING

from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


@as_sudo()
@command(
    help="Rollback only permissions changes on current git repository",
    command_type=COMMAND_TYPE_ADDON,
)
def system__git__rollback_permissions(kernel: Kernel) -> bool:
    from src.helper.command import execute_command_sync

    success, output = execute_command_sync(
        kernel,
        ["git", "diff", "--summary"],
        ignore_error=True,
    )

    if not success:
        return False

    mode_pattern = re.compile(r'^\s*mode change \d+ => \d+ (.+)$')

    files_to_restore = []
    for line in output:
        match = mode_pattern.match(line)
        if match:
            files_to_restore.append(match.group(1))

    if not files_to_restore:
        kernel.io.log("No permission changes to rollback")
        return True

    for file_path in files_to_restore:
        kernel.io.log(f"Rolling back permissions for {file_path}")
        success, _ = execute_command_sync(
            kernel,
            ["git", "checkout", "HEAD", "--", file_path],
            ignore_error=True,
        )
        if not success:
            kernel.io.error(f"Failed to rollback {file_path}")

    return True
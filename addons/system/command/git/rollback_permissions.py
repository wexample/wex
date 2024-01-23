import os
import tempfile
from typing import TYPE_CHECKING

from src.const.types import StringsList
from src.const.globals import COMMAND_TYPE_ADDON
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.helper.command import execute_command_sync

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@as_sudo()
@command(
    help="Rollback only permissions changes on current git repository",
    command_type=COMMAND_TYPE_ADDON,
)
def system__git__rollback_permissions(kernel: "Kernel") -> bool:
    success, diff = execute_command_sync(
        kernel,
        ["git", "diff", "-p", "-R", "--no-ext-diff", "--no-color", "--diff-filter=M"],
        ignore_error=True,
    )

    if not success:
        return False

    current_diff: StringsList = []
    for line in diff:
        if line.startswith("diff"):
            if current_diff:
                _apply_diff(kernel, current_diff)
                current_diff = []
        if line.startswith(("old mode", "new mode", "diff")):
            current_diff.append(line)

    if current_diff:
        _apply_diff(kernel, current_diff)

    return True


def _apply_diff(kernel: "Kernel", diff_lines: StringsList) -> None:
    if len(diff_lines) < 3:
        return

    kernel.io.log(f"Rolling back {diff_lines[0]}")

    diff_str = "\n".join(diff_lines) + "\n"
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_file:
        temp_file.write(diff_str)
        temp_file_path = temp_file.name

    success, _ = execute_command_sync(
        kernel, ["git", "apply", temp_file_path], ignore_error=True
    )

    os.remove(temp_file_path)

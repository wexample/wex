import os
from typing import TYPE_CHECKING

from addons.app.command.webhook.stop import app__webhook__stop
from addons.default.command.file.remove_line import default__file__remove_line
from addons.system.command.system.is_docker import system__system__is_docker
from src.const.globals import CORE_BIN_FILE_LOCAL, CORE_BIN_FILE_ROOT
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.helper.file import file_remove_file_if_exists
from src.helper.user import get_sudo_username, get_user_or_sudo_user_home_data_path

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@as_sudo()
@command(help="Uninstall core")
def core__core__uninstall(kernel: "Kernel") -> None:
    __core__core__uninstall_webhook_server(kernel)
    __core__core__uninstall_symlink(CORE_BIN_FILE_ROOT)
    __core__core__uninstall_symlink(CORE_BIN_FILE_LOCAL)
    __core__core__uninstall_autocomplete(kernel)
    __core__core__uninstall_terminal(kernel)
    kernel.io.log("Bye!")


def __core__core__uninstall_webhook_server(kernel: "Kernel") -> None:
    kernel.run_function(app__webhook__stop)


def __core__core__uninstall_symlink(destination: str) -> None:
    file_remove_file_if_exists(destination)


def __core__core__uninstall_autocomplete(kernel: "Kernel") -> None:
    script_path = "/etc/bash_completion.d/wex"

    file_remove_file_if_exists(script_path)

    __remove_source_file_for_docker(kernel, script_path)


def __core__core__uninstall_terminal(kernel: "Kernel") -> None:
    script_path = "/etc/profile.d/wex"

    file_remove_file_if_exists(script_path)

    __remove_source_file_for_docker(kernel, script_path)


def __remove_source_file_for_docker(kernel: "Kernel", file_path: str) -> None:
    if not kernel.run_function(system__system__is_docker):
        return

    # If sudo has a parent user.
    sudo_user = get_sudo_username()
    if sudo_user:
        __remove_source_file_in_bashrc(
            kernel, file_path, f"{get_user_or_sudo_user_home_data_path()}.bashrc"
        )

    __remove_source_file_in_bashrc(kernel, file_path, os.path.expanduser("~/.bashrc"))


def __remove_source_file_in_bashrc(kernel: "Kernel", file_path: str, bashrc_path: str) -> None:
    if not os.path.exists(bashrc_path):
        return

    kernel.io.log(f"Removing autocompletion script to {bashrc_path}...")

    kernel.run_function(
        default__file__remove_line, {"file-path": bashrc_path, "line": f". {file_path}"}
    )

    kernel.io.message(f"Updated bashrc {bashrc_path}")

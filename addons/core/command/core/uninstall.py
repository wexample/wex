import os

from addons.core.command.webhook.stop import core__webhook__stop
from addons.default.command.file.remove_line import default__file__remove_line
from src.helper.system import get_sudo_username, get_user_or_sudo_user_home_data_path
from addons.system.command.system.is_docker import system__system__is_docker
from src.const.globals import CORE_BIN_FILE_ROOT, CORE_BIN_FILE_LOCAL
from src.decorator.as_sudo import as_sudo
from src.helper.file import remove_file_if_exists
from src.core.Kernel import Kernel
from src.decorator.command import command


@command(help="Uninstall core")
@as_sudo
def core__core__uninstall(kernel: Kernel):
    __core__core__uninstall_webhook_server(kernel)
    __core__core__uninstall_symlink(CORE_BIN_FILE_ROOT)
    __core__core__uninstall_symlink(CORE_BIN_FILE_LOCAL)
    __core__core__uninstall_autocomplete(kernel)
    __core__core__uninstall_terminal(kernel)
    kernel.io.log('Bye!')


def __core__core__uninstall_webhook_server(kernel):
    kernel.run_function(
        core__webhook__stop
    )


def __core__core__uninstall_symlink(destination: str):
    remove_file_if_exists(destination)


def __core__core__uninstall_autocomplete(kernel):
    script_path = '/etc/bash_completion.d/wex'

    remove_file_if_exists(script_path)

    __remove_source_file_for_docker(kernel, script_path)


def __core__core__uninstall_terminal(kernel):
    script_path = '/etc/profile.d/wex'

    remove_file_if_exists(script_path)

    __remove_source_file_for_docker(kernel, script_path)


def __remove_source_file_for_docker(kernel, file_path):
    if not kernel.run_function(system__system__is_docker):
        return

    # If sudo has a parent user.
    sudo_user = get_sudo_username()
    if sudo_user:
        __remove_source_file_in_bashrc(kernel, file_path, f'{get_user_or_sudo_user_home_data_path()}.bashrc')

    __remove_source_file_in_bashrc(kernel, file_path, os.path.expanduser('~/.bashrc'))


def __remove_source_file_in_bashrc(kernel, file_path, bashrc_path):
    if not os.path.exists(bashrc_path):
        return

    kernel.io.log(f'Removing autocompletion script to {bashrc_path}...')

    kernel.run_function(
        default__file__remove_line,
        {
            'file-path': bashrc_path,
            'line': f'. {file_path}'
        }
    )

    kernel.io.message(f'Updated bashrc {bashrc_path}')

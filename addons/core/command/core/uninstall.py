import click

from addons.core.command.webhook.stop import core__webhook__stop
from addons.default.command.file.remove_line import default__file__remove_line
from src.helper.core import get_bashrc_handler_path, get_bashrc_handler_command
from src.const.globals import CORE_BIN_FILE
from src.decorator.as_sudo import as_sudo
from src.helper.file import remove_file_if_exists


@click.command()
@click.pass_obj
@as_sudo
def core__core__uninstall(kernel):
    __core__core__uninstall_webhook_server(kernel)
    __core__core__uninstall_symlink()
    __core__core__uninstall_bashrc(kernel)
    kernel.log('Bye!')


def __core__core__uninstall_webhook_server(kernel):
    kernel.exec_function(
        core__webhook__stop
    )


def __core__core__uninstall_symlink():
    remove_file_if_exists(CORE_BIN_FILE)


def __core__core__uninstall_bashrc(kernel):
    bashrc_handler_path = get_bashrc_handler_path(kernel)
    bashrc_handler_command = get_bashrc_handler_command(kernel)
    kernel.log(f'Removing autocompletion script to {bashrc_handler_path}...')

    kernel.exec_function(
        default__file__remove_line,
        {
            'file-path': bashrc_handler_path,
            'line': bashrc_handler_command
        }
    )

    kernel.message(f'Updated bashrc {bashrc_handler_path}')

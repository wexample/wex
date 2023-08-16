
import click
import os

from addons.default.command.file.append_once import default__file__append_once
from addons.core.command.logo.show import core__logo__show
from addons.core.command.webhook.serve import core__webhook__serve
from src.helper.core import get_bashrc_handler_command, get_bashrc_handler_path
from src.helper.file import remove_file_if_exists
from src.const.globals import CORE_BIN_FILE
from src.decorator.as_sudo import as_sudo


@click.command()
@click.pass_obj
@as_sudo
def core__core__install(kernel):
    __core__core__install_bashrc(kernel)
    __core__core__install_symlink(kernel)
    __core__core__install_webhook_server(kernel)
    return kernel.exec_function(core__logo__show)


def __core__core__install_bashrc(kernel):
    bashrc_path = os.path.expanduser("~/.bashrc")

    if not os.path.exists(bashrc_path):
        with open(bashrc_path, 'w') as f:
            pass

    bashrc_handler_path = get_bashrc_handler_path(kernel)
    bashrc_handler_command = get_bashrc_handler_command(kernel)
    kernel.log(f'Adding autocompletion script to {bashrc_handler_path}...')

    kernel.exec_function(
        default__file__append_once,
        {
            'file': bashrc_handler_path,
            'line': bashrc_handler_command
        }
    )

    kernel.message(f'Updated bashrc {bashrc_handler_path}')


def __core__core__install_symlink(kernel):
    remove_file_if_exists(CORE_BIN_FILE)

    os.symlink(
        kernel.path['core.cli'],
        CORE_BIN_FILE
    )

    os.chmod(CORE_BIN_FILE, 0o755)

    kernel.message(f'Created symlink in {CORE_BIN_FILE}')


def __core__core__install_webhook_server(kernel):
    kernel.exec_function(
        core__webhook__serve,
        {
            'asynchronous': True,
            'force': True
        }
    )

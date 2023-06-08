
import click
import os
import pwd

from addons.default.command.file.append_once import default__file__append_once
from addons.core.command.logo.show import core__logo__show
from addons.core.command.webhook.serve import core__webhook__serve
from src.const.globals import CORE_BIN_FILE
from src.helper.command import execute_command
from src.helper.system import get_sudo_user_home_path, get_sudo_username, get_sudo_gid
from src.decorator.as_sudo import as_sudo


@click.command()
@click.pass_obj
@as_sudo
def core__core__install(kernel):
    __core__core__install_user_home(kernel)
    __core__core__install_bashrc(kernel)
    __core__core__install_symlink(kernel)
    __core__core__install_daemon(kernel)
    return kernel.exec_function(core__logo__show)


def __core__core__install_user_home(kernel):
    user_home_path = get_sudo_user_home_path()
    user = get_sudo_username()

    # Check if user directory exists, create it if missing
    if not os.path.isdir(user_home_path):
        os.makedirs(user_home_path)

        uid = pwd.getpwnam(user).pw_uid

        os.chown(
            user_home_path,
            uid,
            get_sudo_gid()
        )

        # Mark dir as default for this user.
        execute_command(kernel, [
            'usermod',
            '-d',
            user_home_path,
            user
        ])

    kernel.message('User folder exists ' + user_home_path)


def __core__core__install_bashrc(kernel):
    bashrc_path = os.path.expanduser("~/.bashrc")

    if not os.path.exists(bashrc_path):
        with open(bashrc_path, 'w') as f:
            pass

    bashrc_handler_path = os.path.join(kernel.path['root'], 'cli', "bashrc-handler")
    bashrc_handler_command = f'. {bashrc_handler_path}'
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
    if os.path.islink(CORE_BIN_FILE):
        os.remove(CORE_BIN_FILE)

    os.symlink(
        kernel.path['core.cli'],
        CORE_BIN_FILE
    )

    os.chmod(CORE_BIN_FILE, 0o755)

    kernel.message(f'Created symlink in {CORE_BIN_FILE}')


def __core__core__install_daemon(kernel):
    kernel.exec_function(
        core__webhook__serve,
        {
            'asynchronous': True,
            'force': True
        }
    )

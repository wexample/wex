import os
import sys

from addons.app.const.app import APP_ENV_LOCAL
from addons.app.helpers.app import create_env
from addons.core.command.logo.show import core__logo__show
from addons.core.command.webhook.serve import core__webhook__serve
from addons.default.command.file.append_once import default__file__append_once
from addons.system.command.system.is_docker import system__system__is_docker
from src.const.error import ERR_PYTHON_MINIMAL_VERSION
from src.helper.system import get_sudo_username, get_user_or_sudo_user_home_data_path
from src.helper.file import remove_file_if_exists, create_from_template
from src.const.globals import CORE_BIN_FILE_ROOT, PYTHON_MIN_VERSION, CORE_BIN_FILE_LOCAL
from src.decorator.as_sudo import as_sudo
from src.core.Kernel import Kernel
from src.decorator.command import command


@command(help="Install core")
@as_sudo
def core__core__install(kernel: Kernel):
    __core__core__check_requirements(kernel)
    __core__core__install_env(kernel)
    __core__core__install_terminal(kernel)
    __core__core__install_autocomplete(kernel)
    __core__core__install_symlink(kernel, CORE_BIN_FILE_ROOT)
    __core__core__install_symlink(kernel, CORE_BIN_FILE_LOCAL)
    __core__core__install_webhook_server(kernel)
    return kernel.run_function(core__logo__show)


def __core__core__check_requirements(kernel):
    kernel.log(f'Checking python version ...')

    if sys.version_info < PYTHON_MIN_VERSION:
        kernel.error(ERR_PYTHON_MINIMAL_VERSION, {
            'current': '.'.join(str(n) for n in sys.version_info),
            'expected': '.'.join(str(n) for n in PYTHON_MIN_VERSION)
        })


def __core__core__install_env(kernel):
    kernel.log(f'Creating local env ...')

    create_env(
        APP_ENV_LOCAL,
        kernel.path['root']
    )


def __core__core__install_terminal(kernel):
    handler_path = os.path.join(kernel.path['root'], 'cli/terminal-handler')
    script_path = '/etc/profile.d/wex'
    kernel.log(f'Adding terminal initialisation script in {script_path} sourcing {handler_path} ...')

    create_from_template(
        kernel.path['templates'] + 'handler.sh.tpl',
        script_path,
        {
            'handler_path': handler_path,
        }
    )

    __source_file_for_docker(kernel, script_path)


def __core__core__install_autocomplete(kernel):
    handler_path = os.path.join(kernel.path['root'], 'cli/autocomplete-handler')
    script_path = '/etc/bash_completion.d/wex'
    kernel.log(f'Adding autocompletion handler in {script_path} sourcing {handler_path} ...')

    create_from_template(
        kernel.path['templates'] + 'handler.sh.tpl',
        script_path,
        {
            'handler_path': handler_path,
        }
    )

    __source_file_for_docker(kernel, script_path)


def __core__core__install_symlink(kernel, destination: str):
    remove_file_if_exists(destination)

    os.symlink(
        kernel.path['core.cli'],
        destination
    )

    os.chmod(destination, 0o755)

    kernel.log(f'Created symlink in {destination}')


def __core__core__install_webhook_server(kernel):
    kernel.log(f'Installing webhooks server ...')

    kernel.run_function(
        core__webhook__serve,
        {
            'asynchronous': True,
            'force': True
        }
    )


def __source_file_for_docker(kernel, file_path):
    if not kernel.run_function(system__system__is_docker):
        return

    kernel.log(f'Installing Docker container specific setup ...')

    # If sudo has a parent user.
    sudo_user = get_sudo_username()
    if sudo_user:
        __source_file_in_bashrc(kernel, file_path, f'{get_user_or_sudo_user_home_data_path()}.bashrc')

    __source_file_in_bashrc(kernel, file_path, os.path.expanduser('~/.bashrc'))


def __source_file_in_bashrc(kernel, file_path, bashrc_path):
    if not os.path.exists(bashrc_path):
        return

    kernel.log(f'Adding script to {bashrc_path}...')

    kernel.run_function(
        default__file__append_once,
        {
            'file': bashrc_path,
            'line': f'. {file_path}'
        }
    )

    kernel.log(f'Updated bashrc {bashrc_path}')

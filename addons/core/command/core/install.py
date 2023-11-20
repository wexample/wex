import os
import sys

from addons.app.const.app import APP_ENV_LOCAL
from addons.app.helper.app import app_create_env
from addons.core.command.logo.show import core__logo__show
from addons.app.command.webhook.listen import app__webhook__listen
from addons.default.command.file.append_once import default__file__append_once
from src.helper.user import get_sudo_username, get_user_or_sudo_user_home_data_path
from src.helper.file import file_remove_file_if_exists, file_create_from_template
from src.const.globals import CORE_BIN_FILE_ROOT, PYTHON_MIN_VERSION, CORE_BIN_FILE_LOCAL
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@as_sudo()
@command(help="Install core")
def core__core__install(kernel: 'Kernel'):
    __core__core__check_requirements(kernel)
    __core__core__install_env(kernel)
    __core__core__install_terminal(kernel)
    __core__core__install_autocomplete(kernel)
    __core__core__install_symlink(kernel, CORE_BIN_FILE_ROOT)
    __core__core__install_symlink(kernel, CORE_BIN_FILE_LOCAL)
    __core__core__install_webhook_server(kernel)
    __core__core__install_rebuild(kernel)
    return kernel.run_function(core__logo__show)


def __core__core__check_requirements(kernel):
    kernel.io.log(f'Checking python version ...')

    if sys.version_info < PYTHON_MIN_VERSION:
        kernel.io.error("Python {expected} or later is required, actually running on {current}", {
            'current': '.'.join(str(n) for n in sys.version_info),
            'expected': '.'.join(str(n) for n in PYTHON_MIN_VERSION)
        }, trace=False)


def __core__core__install_env(kernel):
    kernel.io.log(f'Creating local env ...')

    app_create_env(
        APP_ENV_LOCAL,
        kernel.get_path('root'),
        False
    )


def __core__core__install_terminal(kernel):
    handler_path = os.path.join(kernel.get_path('root'), 'cli/terminal-handler')
    script_path = '/etc/profile.d/wex'
    kernel.io.log(f'Adding terminal initialisation script in {script_path} sourcing {handler_path} ...')

    file_create_from_template(
        kernel.get_path('templates') + 'handler.sh.tpl',
        script_path,
        {
            'handler_path': handler_path,
        }
    )

    __source_file(kernel, script_path)


def __core__core__install_autocomplete(kernel):
    handler_path = os.path.join(kernel.get_path('root'), 'cli/autocomplete-handler')
    script_path = '/etc/bash_completion.d/wex'
    kernel.io.log(f'Adding autocompletion handler in {script_path} sourcing {handler_path} ...')

    file_create_from_template(
        kernel.get_path('templates') + 'handler.sh.tpl',
        script_path,
        {
            'handler_path': handler_path,
        }
    )

    __source_file(kernel, script_path)


def __core__core__install_symlink(kernel, destination: str):
    file_remove_file_if_exists(destination)

    os.symlink(
        kernel.get_path('core.cli'),
        destination
    )

    os.chmod(destination, 0o755)

    kernel.io.log(f'Created symlink in {destination}')


def __core__core__install_webhook_server(kernel):
    kernel.io.log(f'Installing webhooks server ...')

    kernel.run_function(
        app__webhook__listen,
        {
            'asynchronous': True,
            'force': True
        }
    )


def __core__core__install_rebuild(kernel):
    kernel.rebuild()


def __source_file(kernel, file_path):
    kernel.io.log(f'Sourcing file {file_path} in bashrc ...')

    # If sudo has a parent user.
    sudo_user = get_sudo_username()
    if sudo_user:
        __source_file_in_bashrc(kernel, file_path, f'{get_user_or_sudo_user_home_data_path()}.bashrc')

    __source_file_in_bashrc(kernel, file_path, os.path.expanduser('~/.bashrc'))


def __source_file_in_bashrc(kernel, file_path, bashrc_path):
    if not os.path.exists(bashrc_path):
        return

    kernel.io.log(f'Adding script to {bashrc_path}...')

    kernel.run_function(
        default__file__append_once,
        {
            'file': bashrc_path,
            'line': f'. {file_path}'
        }
    )

    kernel.io.log(f'Updated bashrc {bashrc_path}')

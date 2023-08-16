import click
import os

from addons.app.const.app import APP_ENV_LOCAL
from addons.app.helpers.app import create_env
from addons.core.command.logo.show import core__logo__show
from addons.core.command.webhook.serve import core__webhook__serve
from addons.default.command.file.append_once import default__file__append_once
from addons.system.command.system.is_docker import system__system__is_docker
from src.helper.system import get_sudo_username, get_sudo_user_home_path
from src.helper.file import remove_file_if_exists, create_from_template
from src.const.globals import CORE_BIN_FILE
from src.decorator.as_sudo import as_sudo


@click.command()
@click.pass_obj
@as_sudo
def core__core__install(kernel):
    __core__core__install_env(kernel)
    __core__core__install_terminal(kernel)
    __core__core__install_autocomplete(kernel)
    __core__core__install_symlink(kernel)
    __core__core__install_webhook_server(kernel)
    return kernel.exec_function(core__logo__show)


def __core__core__install_env(kernel):
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
        '/etc/bash_completion.d/wex',
        {
            'handler_path': handler_path,
        }
    )

    __source_file_for_docker(kernel, script_path)


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


def __source_file_for_docker(kernel, file_path):
    if not kernel.exec_function(system__system__is_docker):
        return

    # If sudo has a parent user.
    sudo_user = get_sudo_username()
    if sudo_user:
        __source_file_in_bashrc(kernel, file_path, f'{get_sudo_user_home_path()}.bashrc')

    __source_file_in_bashrc(kernel, file_path, os.path.expanduser('~/.bashrc'))


def __source_file_in_bashrc(kernel, file_path, bashrc_path):
    if not os.path.exists(bashrc_path):
        return

    kernel.log(f'Adding script to {bashrc_path}...')

    kernel.exec_function(
        default__file__append_once,
        {
            'file': bashrc_path,
            'line': f'. {file_path}'
        }
    )

    kernel.message(f'Updated bashrc {bashrc_path}')

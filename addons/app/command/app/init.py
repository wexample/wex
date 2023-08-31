import datetime
import getpass
import yaml
import os.path
import click
from pathlib import Path
from git import Repo
from typing import Iterable, Union

from src.helper.core import core_kernel_get_version
from src.helper.prompt import build_progress_bar
from src.helper.string import to_snake_case, to_kebab_case
from src.helper.args import split_arg_array

from addons.app.command.app.start import app__app__start
from addons.app.decorator.app_location_optional import app_location_optional
from addons.core.command.service.resolve import core__service__resolve
from addons.app.const.app import ERR_SERVICE_NOT_FOUND, APP_DIR_APP_DATA, APP_FILEPATH_REL_CONFIG
from addons.app.const.app import APP_ENV_PROD
from addons.app.helpers.app import create_env
from addons.app.command.service.install import app__service__install
from addons.app.command.hook.exec import app__hook__exec
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel

@click.command
@click.pass_obj
@app_location_optional
@click.option('--name', '-n', type=str, required=False,
              help="Name of new app")
@click.option('--git', '-g', is_flag=True, required=False, default=True,
              help="Initialize GIT repo")
@click.option('--app-dir', '-a', type=str, required=False,
              help="App directory")
@click.option('--services', '-s', type=str, required=False,
              help="List of services to install")
@click.option('--domains', '-d', type=str, required=False,
              help="Comma separated list of domains names")
def app__app__init(
        kernel: Kernel,
        app_dir: str,
        name: str = None,
        services: Union[str, Iterable] = None,
        domains: str = '',
        git: bool = True
):
    manager: AppAddonManager = kernel.addons['app']

    if not app_dir:
        app_dir = os.getcwd() + '/'

    def init_step_check_vars():
        nonlocal name

        kernel.log(f'Creating app in "{app_dir}"')

        if not name:
            name = os.path.basename(
                os.path.dirname(app_dir)
            )

        # Cleanup name.
        name = to_snake_case(name)

        kernel.log(f'Using name "{name}"')

        if not os.path.exists(app_dir):
            os.makedirs(app_dir, exist_ok=True)

    def init_step_check_services():
        nonlocal services
        nonlocal kernel

        services = split_arg_array(services)
        if len(services) == 0:
            return

        # Resolve dependencies for all services
        services = kernel.exec_function(
            core__service__resolve,
            {
                'service': services
            }
        )

        kernel.log('Checking services...')
        for service in services:
            if not service in kernel.registry['services']:
                import logging

                kernel.error(
                    ERR_SERVICE_NOT_FOUND,
                    {
                        'service': service
                    },
                    logging.ERROR
                )

                return False

    def init_step_copy_app():
        import shutil

        app_sample_dir = os.path.join(kernel.path['addons'], 'app', 'samples', 'app') + '/'

        os.makedirs(os.path.join(app_dir, APP_DIR_APP_DATA), exist_ok=True)

        shutil.copytree(
            app_sample_dir + APP_DIR_APP_DATA,
            os.path.join(
                app_dir,
                APP_DIR_APP_DATA
            ),
            dirs_exist_ok=True,
            copy_function=shutil.copy2
        )

        kernel.log('Renaming .sample files...')
        # Remove every .sample suffix after filenames
        # i.e .gitignore.sample becomes .gitignore
        app_data_path = os.path.join(app_dir, APP_DIR_APP_DATA)
        sample_files = list(Path(app_data_path).rglob('*.sample'))

        for sample_file in sample_files:
            new_file_name = os.path.splitext(sample_file)[0]
            os.rename(sample_file, new_file_name)
            kernel.log(f'Renaming {sample_file}')

    def init_step_create_env():
        kernel.log(f'Creating env file with env "{APP_ENV_PROD}"')
        create_env(
            APP_ENV_PROD,
            app_dir
        )

    def init_step_create_config():
        nonlocal domains

        kernel.log(f'Creating config...')

        domains = split_arg_array(domains)
        domains_main = domains[0] if domains else f'{to_kebab_case(name)}.wex'
        email = f'contact@{domains_main}'

        config = {
            'global': {
                'author': getpass.getuser(),
                'created': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'name': name,
                'services': [],
            },
            'docker': {
                'compose': {
                    'tty': True,
                    'stdin_open': True,
                }
            },
            'env': {
                'local': {
                    'domains': f'{name}.wex',
                    'domain_main': f'{name}.wex',
                    'email': email
                },
                'dev': {
                    'domains': domains.copy(),
                    'domain_main': domains_main,
                    'email': email
                },
                'prod': {
                    'domains': domains.copy(),
                    'domain_main': domains_main,
                    'email': email
                }
            },
            'wex': {
                'version': core_kernel_get_version(kernel)
            }
        }

        with open(app_dir + APP_FILEPATH_REL_CONFIG, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

    def init_step_set_workdir():
        nonlocal manager

        manager.set_app_workdir(app_dir)

    def init_step_install_service():
        nonlocal services
        nonlocal kernel

        kernel.log('Installing services...')
        for service in services:
            services = kernel.exec_function(
                app__service__install,
                {
                    'app-dir': app_dir,
                    'service': service,
                    # Dependencies have already been resolved
                    'ignore-dependencies': True
                }
            )

    def init_step_init_git():
        nonlocal git

        if git:
            kernel.log('Installing git repo...')

            Repo.init(app_dir)

    def init_step_hooks():
        kernel.exec_function(
            app__hook__exec,
            {
                'app-dir': app_dir,
                'hook': 'app/init-post'
            }
        )

    def init_step_unset_workdir():
        manager.unset_app_workdir()

    steps = [
        init_step_check_vars,
        init_step_check_services,
        init_step_copy_app,
        init_step_create_env,
        init_step_create_config,
        init_step_set_workdir,
        init_step_install_service,
        init_step_init_git,
        init_step_hooks,
        init_step_unset_workdir,
    ]

    with build_progress_bar(steps, label="Initialization") as progress_bar:
        for step in progress_bar:
            kernel.log(f'Init step : {step.__name__}')
            kernel.log_indent_up()

            response = step()

            kernel.log_indent_down()
            click.echo("\n")

            # Step failed somewhere
            if response is False:
                return

    kernel.message(f'Your app is initialized as" {name}"')
    kernel.message_next_command(
        app__app__start
    )

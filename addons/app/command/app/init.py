import os.path
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Optional, Union

from git import Repo

from addons.app.command.app.start import app__app__start
from addons.app.command.hook.exec import app__hook__exec
from addons.app.command.service.install import app__service__install
from addons.app.const.app import (APP_DIR_APP_DATA, APP_ENV_LOCAL,
                                  ERR_SERVICE_NOT_FOUND)
from addons.app.decorator.app_command import app_command
from addons.app.helper.app import app_create_env
from addons.core.command.service.resolve import core__service__resolve
from src.const.globals import COMMAND_TYPE_SERVICE
from src.decorator.option import option
from src.helper.args import args_split_arg_array
from src.helper.prompt import prompt_progress_steps
from src.helper.string import string_to_snake_case

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Create new app and services configuration", dir_required=False)
@option('--name', '-n', type=str, required=False,
        help="Name of new app")
@option('--git', '-g', is_flag=True, required=False, default=True,
        help="Initialize GIT repo")
@option('--app-dir', '-a', type=str, required=False,
        help="App directory")
@option('--services', '-s', type=str, required=False,
        help="List of services to install")
@option('--domains', '-d', type=str, required=False,
        help="Comma separated list of domains names")
@option('--env', '-e', type=str, required=False,
        help="App environment")
def app__app__init(
        manager: 'AppAddonManager',
        app_dir: str,
        name: Optional[str] = None,
        services: Optional[Union[str, Iterable]] = None,
        domains: str = '',
        git: bool = True,
        env: str | None = None
):
    kernel = manager.kernel
    current_dir = os.getcwd() + os.sep
    env = env or APP_ENV_LOCAL

    if not app_dir:
        app_dir = current_dir

    def _init_step_check_vars() -> None:
        nonlocal name

        kernel.io.log(f'Creating app in "{app_dir}"')

        if not name:
            name = os.path.basename(
                os.path.dirname(app_dir)
            )

        # Cleanup name.
        name = string_to_snake_case(name)

        kernel.io.log(f'Using name "{name}"')

        if not os.path.exists(app_dir):
            os.makedirs(app_dir, exist_ok=True)

    def _init_step_check_services() -> Optional[bool]:
        nonlocal services
        nonlocal kernel

        services = args_split_arg_array(services)
        if len(services) == 0:
            return

        # Resolve dependencies for all services
        services = kernel.run_function(
            core__service__resolve,
            {
                'service': services
            }
        ).first()

        kernel.io.log('Checking services...')
        for service in services:
            if not service in kernel.resolvers[COMMAND_TYPE_SERVICE].get_registry_data():
                kernel.io.error(
                    ERR_SERVICE_NOT_FOUND,
                    {
                        'service': service
                    }
                )

                return False

    def _init_step_copy_app() -> None:
        import shutil

        app_sample_dir = os.path.join(kernel.get_path('addons'), 'app', 'samples', 'app') + '/'

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

        kernel.io.log('Renaming .sample files...')
        # Remove every .sample suffix after filenames
        # i.e .gitignore.sample becomes .gitignore
        app_data_path = os.path.join(app_dir, APP_DIR_APP_DATA)
        sample_files = list(Path(app_data_path).rglob('*.sample'))

        for sample_file in sample_files:
            new_file_name = os.path.splitext(sample_file)[0]
            os.rename(sample_file, new_file_name)
            kernel.io.log(f'Renaming {sample_file}')

    def _init_step_create_env() -> None:
        kernel.io.log(f'Creating env file with env "{env}"')
        app_create_env(
            env,
            app_dir
        )

    def _init_step_create_config() -> None:
        nonlocal domains
        nonlocal manager

        kernel.io.log(f'Creating config...')

        domains = args_split_arg_array(domains)
        manager.config = manager.create_config(name, domains)

        manager.save_config()

    def _init_step_set_workdir() -> None:
        nonlocal manager

        manager.set_app_workdir(app_dir)

    def _init_step_install_service() -> None:
        nonlocal services
        nonlocal kernel

        kernel.io.log('Installing services...')
        for service in services:
            services = kernel.run_function(
                app__service__install,
                {
                    'app-dir': app_dir,
                    'service': service,
                    # Dependencies have already been resolved
                    'ignore-dependencies': True
                }
            ).first()

    def _init_step_init_git() -> None:
        nonlocal git

        if git:
            kernel.io.log('Installing git repo...')

            Repo.init(app_dir)

    def _init_step_hooks() -> None:
        kernel.run_function(
            app__hook__exec,
            {
                'app-dir': app_dir,
                'hook': 'app/init-post'
            }
        )

    def _init_step_unset_workdir() -> None:
        manager.unset_app_workdir(current_dir)

    def _init_step_complete() -> None:
        kernel.io.message_next_command(
            app__app__start,
            message=f'Your app has been created in {env} environment'
        )

    prompt_progress_steps(kernel, [
        _init_step_check_vars,
        _init_step_check_services,
        _init_step_copy_app,
        _init_step_create_env,
        _init_step_set_workdir,
        _init_step_create_config,
        _init_step_install_service,
        _init_step_init_git,
        _init_step_hooks,
        _init_step_unset_workdir,
        _init_step_complete,
    ])

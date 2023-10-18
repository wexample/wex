import os.path
from pathlib import Path
from git import Repo
from typing import Iterable, Union

from src.helper.prompt import progress_steps
from src.helper.string import to_snake_case
from src.helper.args import split_arg_array
from src.decorator.option import option

from addons.app.command.app.start import app__app__start
from addons.core.command.service.resolve import core__service__resolve
from addons.app.const.app import ERR_SERVICE_NOT_FOUND, APP_DIR_APP_DATA
from addons.app.const.app import APP_ENV_PROD
from addons.app.helpers.app import create_env
from addons.app.command.service.install import app__service__install
from addons.app.command.hook.exec import app__hook__exec
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from src.decorator.alias_without_addon import alias_without_addon
from addons.app.decorator.app_command import app_command


@app_command(help="Create new app and services configuration", dir_required=False)
@alias_without_addon()
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
        kernel: Kernel,
        app_dir: str,
        name: str = None,
        services: Union[str, Iterable] = None,
        domains: str = '',
        git: bool = True,
        env: str | None = None
):
    manager: AppAddonManager = kernel.addons['app']
    current_dir = os.getcwd() + os.sep
    env = env or APP_ENV_PROD

    if not app_dir:
        app_dir = current_dir

    def init_step_check_vars():
        nonlocal name

        kernel.io.log(f'Creating app in "{app_dir}"')

        if not name:
            name = os.path.basename(
                os.path.dirname(app_dir)
            )

        # Cleanup name.
        name = to_snake_case(name)

        kernel.io.log(f'Using name "{name}"')

        if not os.path.exists(app_dir):
            os.makedirs(app_dir, exist_ok=True)

    def init_step_check_services():
        nonlocal services
        nonlocal kernel

        services = split_arg_array(services)
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
            if not service in kernel.registry['services']:
                kernel.io.error(
                    ERR_SERVICE_NOT_FOUND,
                    {
                        'service': service
                    }
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

        kernel.io.log('Renaming .sample files...')
        # Remove every .sample suffix after filenames
        # i.e .gitignore.sample becomes .gitignore
        app_data_path = os.path.join(app_dir, APP_DIR_APP_DATA)
        sample_files = list(Path(app_data_path).rglob('*.sample'))

        for sample_file in sample_files:
            new_file_name = os.path.splitext(sample_file)[0]
            os.rename(sample_file, new_file_name)
            kernel.io.log(f'Renaming {sample_file}')

    def init_step_create_env():
        kernel.io.log(f'Creating env file with env "{env}"')
        create_env(
            env,
            app_dir
        )

    def init_step_create_config():
        nonlocal domains
        nonlocal manager

        kernel.io.log(f'Creating config...')

        domains = split_arg_array(domains)
        manager.config = manager.create_config(name, domains)

        manager.save_config()

    def init_step_set_workdir():
        nonlocal manager

        manager.set_app_workdir(app_dir)

    def init_step_install_service():
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

    def init_step_init_git():
        nonlocal git

        if git:
            kernel.io.log('Installing git repo...')

            Repo.init(app_dir)

    def init_step_hooks():
        kernel.run_function(
            app__hook__exec,
            {
                'app-dir': app_dir,
                'hook': 'app/init-post'
            }
        )

    def init_step_unset_workdir():
        manager.unset_app_workdir(current_dir)

    def init_step_complete():
        kernel.io.message_next_command(
            app__app__start,
            message=f'Your app has been created in {env} environment'
        )

    progress_steps(kernel, [
        init_step_check_vars,
        init_step_check_services,
        init_step_copy_app,
        init_step_create_env,
        init_step_set_workdir,
        init_step_create_config,
        init_step_install_service,
        init_step_init_git,
        init_step_hooks,
        init_step_unset_workdir,
        init_step_complete,
    ])

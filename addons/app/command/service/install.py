import os
import shutil
from typing import TYPE_CHECKING

import yaml

from addons.app.const.app import APP_DIR_APP_DATA
from addons.app.decorator.app_command import app_command
from src.const.globals import (COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON,
                               COMMAND_TYPE_SERVICE)
from src.decorator.option import option
from src.helper.dict import dict_merge
from src.helper.file import file_create_parent_and_touch, file_merge_new_lines
from src.helper.service import service_get_dir
from src.helper.string import string_to_snake_case

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install given service in app configuration")
@option('--service', '-s', type=str, required=True,
        help="Service name")
@option('--install-config', '-ic', type=bool, required=False, is_flag=True, default=True,
        help='Add to config')
@option('--install-docker', '-id', type=bool, required=False, is_flag=True, default=True,
        help='Merge docker files')
@option('--install-git', '-ig', type=bool, required=False, is_flag=True, default=True,
        help='Merge git files')
@option('--force', '-f', type=bool, required=False, is_flag=True, default=False,
        help='Force install even service already installed')
@option('--ignore-dependencies', '-id', type=bool, required=False, is_flag=True, default=False,
        help='Install dependencies')
def app__service__install(
        manager: 'AppAddonManager',
        app_dir: str,
        service: str,
        install_config: bool = True,
        install_docker: bool = True,
        install_git: bool = True,
        force: bool = False,
        ignore_dependencies: bool = False
):
    kernel = manager.kernel
    service = string_to_snake_case(service)
    kernel.io.log(f'Installing service : {service}')

    services_registry = kernel.resolvers[COMMAND_TYPE_SERVICE].get_registry_data()

    if not service in services_registry:
        kernel.io.log('Service does not exists')
        return

    if not ignore_dependencies:
        # Install dependencies
        for dependency in services_registry[service]['config'].get('dependencies', []):
            kernel.io.log(f'Expected dependency : {dependency}')

            app__service__install.function.callback(
                app_dir,
                dependency,
                install_config,
                install_docker,
                install_git,
                force
            )

    services = manager.get_config('service') or {}

    if service in services and not force:
        kernel.io.log('Service already installed')
        return

    if install_config:
        kernel.io.log('Adding to config')
        # Append once, and remove duplicates
        services[service] = {}

        manager.set_config('service', services)

    service_dir = service_get_dir(kernel, service)
    service_sample_dir = os.path.join(service_dir, 'samples') + '/'
    service_sample_dir_env = os.path.join(service_sample_dir, APP_DIR_APP_DATA) + '/'

    if os.path.isdir(service_sample_dir_env):
        items = os.listdir(service_sample_dir_env)

        for item in items:
            app_service_install_merge_dir(
                manager,
                item,
                service_sample_dir,
                app_dir,
                install_docker,
                install_git,
            )

    # Allow service to set global settings
    service_config = services_registry[service]['config']

    # First service is set as main service
    main_service = manager.get_config('global.main_service')
    if not main_service:
        manager.set_config(
            'global.main_service',
            service)

    if 'tags' in service_config and 'db' in service_config['tags']:
        main_db_container = manager.get_config('docker.main_db_container')
        if not main_db_container:
            manager.set_config(
                'docker.main_db_container',
                service)

    if 'global' in service_config:
        config_global = dict_merge(
            manager.get_config('global'),
            service_config['global']
        )

        manager.set_config('global', config_global)

    kernel.run_command(
        f'{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}service/install',
        {
            'app-dir': app_dir,
            'service': service
        },
        quiet=True
    )


def app_service_install_merge_dir(
        manager,
        current_item,
        service_dir,
        app_dir,
        install_docker,
        install_git,
):
    kernel = manager.kernel
    abs_path = os.path.join(service_dir, APP_DIR_APP_DATA, current_item)
    kernel.io.log(f'Merging {current_item}')

    if os.path.isdir(abs_path):
        items = os.listdir(abs_path)

        for item in items:
            app_service_install_merge_dir(
                manager,
                current_item + '/' + item,
                service_dir,
                app_dir,
                install_docker,
                install_git,
            )
    else:
        basename = os.path.basename(abs_path)
        dest_file = os.path.join(
            app_dir,
            APP_DIR_APP_DATA,
            current_item
        )

        if basename == '.gitignore.sample':
            if install_git:
                kernel.io.log('Mixing GIT ignore')

                # Override file name.
                dest_file = os.path.join(
                    app_dir,
                    APP_DIR_APP_DATA,
                    '.gitignore'
                )

                file_create_parent_and_touch(dest_file)

                file_merge_new_lines(
                    abs_path,
                    dest_file
                )
        elif basename.startswith('docker-compose.') and basename.endswith('.yml'):
            if install_docker:
                kernel.io.log('Mixing Docker compose YML')

                file_create_parent_and_touch(dest_file, default='services: {}')

                with open(dest_file, 'r') as f:
                    app_compose = yaml.safe_load(f)
                with open(abs_path, 'r') as f:
                    extra_compose = yaml.safe_load(f) or {}

                app_name = manager.get_config('global.name')

                if 'services' in extra_compose:
                    extra_services = {}
                    for service in extra_compose['services']:
                        extra_services[f'{app_name}_{service}'] = extra_compose['services'][service]

                    extra_compose['services'] = extra_services

                merged_data = dict_merge(app_compose, extra_compose)

                with open(dest_file, 'w') as f:
                    yaml.dump(merged_data, f)
        else:
            file_create_parent_and_touch(dest_file)

            shutil.copy2(
                abs_path,
                dest_file
            )

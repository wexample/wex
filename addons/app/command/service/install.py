import os
import shutil

import click
from addons.app.const.app import ERR_SERVICE_EXISTS, APP_DIR_APP_DATA
from addons.app.helpers.app import config_save
from addons.docker.helpers.docker import merge_docker_compose_files
from src.helper.array import array_unique
from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON
from src.helper.file import merge_new_lines, create_directories_and_file
from src.helper.service import get_service_dir


@click.command
@click.pass_obj
@click.option('--service', '-s', type=str, required=True,
              help="Service name")
@click.option('--app-dir', '-a', type=str, required=True,
              help="App directory")
@click.option('--install-config', '-ic', type=bool, required=False, is_flag=True, default=True,
              help='Add to config')
@click.option('--install-docker', '-id', type=bool, required=False, is_flag=True, default=True,
              help='Merge docker files')
@click.option('--install-git', '-ig', type=bool, required=False, is_flag=True, default=True,
              help='Merge git files')
@click.option('--force', '-f', type=bool, required=False, is_flag=True, default=False,
              help='Force install even service already installed')
def app__service__install(
        kernel,
        app_dir: str,
        service: str,
        install_config: bool = True,
        install_docker: bool = True,
        install_git: bool = True,
        force: bool = False
):
    kernel.log(f'Installing service : {service}')

    # Install dependencies
    for dependency in kernel.registry['services'][service]['config'].get('dependencies', []):
        kernel.log(f'Expected dependency : {dependency}')
        kernel.log_indent_up()

        app__service__install.callback(
            app_dir,
            dependency,
            install_config,
            install_docker,
            install_git,
            force
        )

        kernel.log_indent_down()

    if service in kernel.addons['app']['config']['global']['services'] and not force:
        kernel.error(ERR_SERVICE_EXISTS, {
            'service': service
        })

    if install_config:
        kernel.addons['app']['config']['global']['services'].append(service)
        config_save(kernel)

    # Remove duplicates
    kernel.addons['app']['config']['global']['services'] = array_unique(
        kernel.addons['app']['config']['global']['services'])

    service_dir = get_service_dir(kernel, service)

    service_sample_dir = os.path.join(service_dir, 'samples') + '/'
    service_sample_dir_wex = os.path.join(service_sample_dir, APP_DIR_APP_DATA) + '/'

    if os.path.isdir(service_sample_dir_wex):
        items = os.listdir(service_sample_dir_wex)

        for item in items:
            app_service_install_merge_dir(
                kernel,
                item,
                service_sample_dir,
                app_dir,
                install_docker,
                install_git,
            )

    # Merge service global configuration to root
    config = kernel.addons['app']['config']
    if 'global' in kernel.registry['services'][service]['config']:
        config['global'].update(kernel.registry['services'][service]['config']['global'])

    config_save(kernel)

    kernel.exec(
        f'{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}service/install',
        quiet=True
    )


def app_service_install_merge_dir(
        kernel,
        current_item,
        service_dir,
        app_dir,
        install_docker,
        install_git,
):
    kernel.log_indent_up()

    abs_path = os.path.join(service_dir, APP_DIR_APP_DATA, current_item)
    kernel.log(f'Merging {current_item}')

    if os.path.isdir(abs_path):
        items = os.listdir(abs_path)

        for item in items:
            app_service_install_merge_dir(
                kernel,
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
                kernel.log('GIT ignore')

                # Override file name.
                dest_file = os.path.join(
                    app_dir,
                    APP_DIR_APP_DATA,
                    '.gitignore'
                )

                create_directories_and_file(dest_file)

                merge_new_lines(
                    abs_path,
                    dest_file
                )
        elif basename.startswith('docker-compose.') and basename.endswith('.yml'):
            if install_docker:
                kernel.log('Docker compose YML')

                create_directories_and_file(dest_file)

                merge_docker_compose_files(
                    abs_path,
                    dest_file
                )
        else:
            create_directories_and_file(dest_file)

            shutil.copy2(
                abs_path,
                dest_file
            )

    kernel.log_indent_down()

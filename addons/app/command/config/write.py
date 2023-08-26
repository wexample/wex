import os
import socket
import click

from addons.app.const.app import APP_FILEPATH_REL_DOCKER_ENV, APP_FILEPATH_REL_COMPOSE_BUILD_YML
from addons.app.helpers.app import app_config_to_docker_env, config_save_build
from addons.app.command.env.get import app__env__get
from addons.app.helpers.docker import exec_app_docker_compose, get_app_docker_compose_files
from src.helper.system import set_permissions_recursively, get_gid_from_group_name, \
    get_uid_from_user_name
from src.helper.file import write_dict_to_config
from src.helper.system import get_user_or_sudo_user, get_user_group_name

@click.command
@click.pass_obj
@click.option('--app-dir', '-a', type=str, required=False,
              help="Add directory")
@click.option('--user', '-u', type=str, required=False,
              help="Owner of application files")
@click.option('--group', '-g', type=str, required=False,
              help="Group of application files")
def app__config__write(kernel, app_dir: str = './', user: str = None, group: str = None):
    """Build config file used in docker based on services and base config"""
    config = kernel.addons['app']['config']
    env = app__env__get.callback()
    env_config = config['env'].get(env, {})

    user = user or get_user_or_sudo_user()
    group = group or get_user_group_name(user)

    kernel.log(f'Using user {user}:{group}')
    set_permissions_recursively(user, group, app_dir)

    config['context'].update({
        'env': env,
        'host': {
            'ip': socket.gethostbyname(
                socket.gethostname()
            )
        },
        'name': f'{config["global"]["name"]}_{env}',
        'started': False,
        'user': {
            'group': group,
            'gid': get_gid_from_group_name(group),
            'name': user,
            'uid': get_uid_from_user_name(user),
        }
    })

    config['context'].update(env_config)
    config['service'] = {}

    # Build paths to services docker compose yml files.
    for service, service_data in kernel.registry['services'].items():
        base_yml = service_data['dir'] + 'docker/docker-compose.yml'
        env_yml = service_data['dir'] + f'docker/docker-compose.{env}.yml'

        if not os.path.exists(env_yml):
            env_yml = base_yml

        config['service'][service] = {
            'yml': {
                'base': base_yml,
                'env': env_yml,
            }
        }

    kernel.log(f'Build config file')
    kernel.addons['app']['config_build'] = kernel.addons['app']['config']
    config_save_build(kernel)

    # Write as docker env file
    write_dict_to_config(
        app_config_to_docker_env(
            dict(
                sorted(
                    config.items()
                )
            )
        ),
        APP_FILEPATH_REL_DOCKER_ENV
    )

    kernel.log(f'Creating docker compose file')
    yml_content = exec_app_docker_compose(
        kernel,
        get_app_docker_compose_files(
            kernel,
            app_dir
        ),
        'config'
    )

    with open(APP_FILEPATH_REL_COMPOSE_BUILD_YML, 'w') as f:
        f.write(yml_content)

import os
import socket
import click

from addons.app.const.app import APP_FILEPATH_REL_COMPOSE_BUILD_YML, APP_DIR_APP_DATA
from addons.app.helpers.app import config_save_build
from addons.app.command.env.get import app__env__get
from addons.app.helpers.docker import exec_app_docker_compose, get_app_docker_compose_files
from src.helper.dict import merge_dicts
from src.const.globals import PASSWORD_INSECURE
from src.helper.system import get_gid_from_group_name, \
    get_uid_from_user_name
from src.helper.system import get_user_or_sudo_user, get_user_group_name
from addons.app.helpers.app import app_log
from addons.app.command.hook.exec import app__hook__exec


@click.command
@click.pass_obj
@click.option('--app-dir', '-a', type=str, required=False,
              help="Add directory")
@click.option('--user', '-u', type=str, required=False,
              help="Owner of application files")
@click.option('--group', '-g', type=str, required=False,
              help="Group of application files")
def app__config__write(kernel, app_dir: str, user: str = None, group: str = None):
    """Build config file used in docker based on services and base config"""
    config_build = kernel.addons['app']['config'].copy()
    env = app__env__get.callback(app_dir)
    env_config = config_build['env'].get(env, {})
    user = user or get_user_or_sudo_user()
    group = group or get_user_group_name(user)

    app_log(kernel, f'Using user {user}:{group}')

    config_build['context'].update({
        'dir': app_dir,
        'env': env,
        'host': {
            'ip': socket.gethostbyname(
                socket.gethostname()
            )
        },
        'name': f'{config_build["global"]["name"]}_{env}',
        'started': False,
        'user': {
            'group': group,
            'gid': get_gid_from_group_name(group),
            'name': user,
            'uid': get_uid_from_user_name(user),
        }
    })

    config_build['context'].update(env_config)
    config_build['service'] = {}

    # Build paths to services docker compose yml files.
    for service, service_data in kernel.registry['services'].items():
        base_yml = service_data['dir'] + 'docker/docker-compose.yml'
        env_yml = service_data['dir'] + f'docker/docker-compose.{env}.yml'

        if not os.path.exists(env_yml):
            env_yml = base_yml

        config_build['service'][service] = {
            'yml': {
                'base': base_yml,
                'env': env_yml,
            }
        }

    app_log(kernel, f'Build config file')

    config_build = merge_dicts(
        config_build,
        {
            'context': {
                'call_working_dir': os.getcwd(),
                'dir_wex': app_dir + APP_DIR_APP_DATA,
            },
            'password': {
                'insecure': PASSWORD_INSECURE
            }
        }
    )

    kernel.addons['app']['config_build'] = config_build

    config_save_build(
        kernel,
        app_dir
    )

    kernel.exec_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'config/write-compose-pre'
        }
    )

    compose_files = get_app_docker_compose_files(
        kernel,
        app_dir
    )

    if len(compose_files) != 0:
        manager.log(f'Creating docker compose file...')

        yml_content = exec_app_docker_compose(
            kernel,
            app_dir,
            compose_files,
            'config'
        )

        with open(APP_FILEPATH_REL_COMPOSE_BUILD_YML, 'w') as f:
            f.write(yml_content)

    kernel.exec_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'config/write-post'
        }
    )

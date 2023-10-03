import os

from addons.app.const.app import APP_FILEPATH_REL_DOCKER_ENV
from addons.app.command.service.used import app__service__used
from addons.app.const.app import APP_DIR_APP_DATA
from addons.docker.helpers.docker import user_has_docker_permission
from addons.app.AppAddonManager import AppAddonManager
from src.helper.command import execute_command
from src.helper.system import get_user_or_sudo_user
from src.helper.process import process_post_exec
from src.const.error import ERR_UNEXPECTED, ERR_USER_HAS_NO_DOCKER_PERMISSION


def get_app_docker_compose_files(kernel, app_dir):
    app_compose_file = app_dir + APP_DIR_APP_DATA + 'docker/docker-compose.yml'
    compose_files = []

    if not os.path.isfile(app_compose_file):
        return compose_files

    if kernel.run_function(app__service__used, {
        'app-dir': app_dir,
        'service': 'proxy',
    }):
        compose_files.append(kernel.path['addons'] + 'app/containers/network/docker-compose.yml')
    else:
        compose_files.append(kernel.path['addons'] + 'app/containers/default/docker-compose.yml')

    compose_files.append(
        app_compose_file
    )

    manager: AppAddonManager = kernel.addons['app']
    env = manager.get_runtime_config('env')

    env_yml = f'{app_dir}{APP_DIR_APP_DATA}docker/docker-compose.{env}.yml'
    if os.path.isfile(env_yml):
        compose_files.append(env_yml)

    return compose_files


def exec_app_docker_compose_command(
        kernel,
        app_dir: str,
        compose_files,
        docker_command,
        profile=None,
        sync=True
):
    username = get_user_or_sudo_user()
    if not user_has_docker_permission(username):
        kernel.io.error(ERR_USER_HAS_NO_DOCKER_PERMISSION, {
            'username': username
        })

    manager: AppAddonManager = kernel.addons['app']
    env = manager.get_runtime_config('env')

    command = [
        'docker',
        'compose',
    ]

    for file in compose_files:
        command.append('-f')

        command.append(os.path.realpath(file))

    command += [
        '--profile',
        (profile or f'env_{env}'),
        '--env-file',
        os.path.join(
            app_dir,
            APP_FILEPATH_REL_DOCKER_ENV
        ),
    ]

    if type(docker_command) == str:
        docker_command = [docker_command]

    return command + docker_command


def exec_app_docker_compose(
        kernel,
        app_dir: str,
        compose_files,
        docker_command,
        profile=None,
        sync=True
):
    command = exec_app_docker_compose_command(
        kernel,
        app_dir,
        compose_files,
        docker_command,
        profile,
        sync
    )

    if sync:
        success, output = execute_command(kernel, command)

        if not success:
            kernel.io.error(
                ERR_UNEXPECTED,
                {
                    'error': f'Error during running docker compose "{docker_command}" : \n\n'
                             + ' '.join(command)
                             + '\n'.join(output)
                }
            )

        return '\n'.join(output)

    process_post_exec(kernel, command)

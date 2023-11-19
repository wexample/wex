import json
import os
import subprocess

from addons.app.const.app import APP_FILEPATH_REL_DOCKER_ENV
from addons.app.const.app import APP_DIR_APP_DATA
from addons.docker.helper.docker import user_has_docker_permission
from src.helper.command import execute_command
from src.helper.system import get_user_or_sudo_user
from src.helper.process import process_post_exec


def get_app_docker_compose_files(kernel, app_dir):
    from addons.app.AppAddonManager import AppAddonManager
    from addons.app.command.service.used import app__service__used

    app_compose_file = app_dir + APP_DIR_APP_DATA + 'docker/docker-compose.yml'
    compose_files = []

    if not os.path.isfile(app_compose_file):
        return compose_files

    if kernel.run_function(app__service__used, {
        'app-dir': app_dir,
        'service': 'proxy',
    }).first():
        compose_files.append(kernel.get_path('addons') + 'app/containers/network/docker-compose.yml')
    else:
        compose_files.append(kernel.get_path('addons') + 'app/containers/default/docker-compose.yml')

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
):
    username = get_user_or_sudo_user()
    if not user_has_docker_permission(username):
        kernel.io.error(
            f"User should have permission to run Docker. To give permission, add user to docker group : {os.linesep} sudo "
            "usermod -aG docker {username}", {
                'username': username
            }, trace=False)

    manager = kernel.addons['app']
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
    )

    if sync:
        success, output = execute_command(kernel, command)

        if not success:
            kernel.io.error(
                f'Error during running docker compose "{docker_command}" : {os.linesep}{os.linesep}'
                + ' '.join(command)
                + os.linesep.join(output),
                trace=False
            )

        return os.linesep.join(output)

    process_post_exec(kernel, command)


def get_container_pid(container_name):
    cmd = f"docker inspect {container_name}"
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    data = json.loads(result.stdout.decode('utf-8'))
    return data[0]['State']['Pid']


def build_long_container_name(kernel, name: str) -> str:
    manager = kernel.addons['app']
    return f'{manager.get_runtime_config("name")}_{name}'

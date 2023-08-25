import os
import subprocess

from addons.app.const.app import APP_FILEPATH_REL_DOCKER_ENV
from addons.app.command.service.used import app__service__used
from addons.app.const.app import APP_DIR_APP_DATA
from addons.app.command.env.get import app__env__get
from src.helper.process import process_post_exec
from src.const.error import ERR_UNEXPECTED


def get_app_docker_compose_files(kernel, app_dir):
    compose_files = []
    if kernel.exec_function(app__service__used, {
        'app-dir': app_dir,
        'service': 'proxy',
    }):
        compose_files.append(kernel.path['addons'] + 'app/containers/default/docker-compose.yml')
    else:
        compose_files.append(kernel.path['addons'] + 'app/containers/network/docker-compose.yml')

    compose_files.append(
        app_dir + APP_DIR_APP_DATA + 'docker/docker-compose.yml'
    )

    env_yml = app_dir + APP_DIR_APP_DATA + 'docker/docker-compose.' + app__env__get.callback(app_dir=app_dir) + '.yml'
    if os.path.isfile(env_yml):
        compose_files.append(env_yml)

    return compose_files


def exec_app_docker_compose(
        kernel,
        compose_files,
        command,
        profile=None,
        sync=True
):
    env = app__env__get.callback()

    args = [
        'docker',
        'compose',
    ]

    for file in compose_files:
        args.append('-f')
        args.append(file)

    args += [
        '--profile',
        (profile or f'env_{env}'),
        '--env-file',
        APP_FILEPATH_REL_DOCKER_ENV,
    ]

    if type(command) == str:
        command = [command]

    args += command

    if sync:
        result = subprocess.run(args, capture_output=True, text=True)

        if result.stderr:
            kernel.error(
                ERR_UNEXPECTED,
                {
                    'error': f'Error during running docker compose "{command}" : {result.stderr}'
                }
            )

        return str(result.stdout)

    process_post_exec(kernel, args)
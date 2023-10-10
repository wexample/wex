import os
import socket

from addons.app.const.app import APP_FILEPATH_REL_COMPOSE_RUNTIME_YML, APP_DIR_APP_DATA
from addons.app.command.env.get import app__env__get
from addons.app.helpers.docker import exec_app_docker_compose, get_app_docker_compose_files
from src.const.globals import PASSWORD_INSECURE
from src.helper.system import get_gid_from_group_name, \
    get_uid_from_user_name
from src.helper.system import get_user_or_sudo_user, get_user_group_name
from addons.app.command.hook.exec import app__hook__exec
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse


@command(help="Write the configuration file for services to start")
@option('--app-dir', '-a', type=str, required=False,
        help="Add directory")
@option('--user', '-u', type=str, required=False,
        help="Owner of application files")
@option('--group', '-g', type=str, required=False,
        help="Group of application files")
def app__config__write(kernel: Kernel, app_dir: str, user: str = None, group: str = None):
    """Build config file used in docker based on services and base config"""
    manager: AppAddonManager = kernel.addons['app']

    def _app__config__write__runtime():
        nonlocal user
        nonlocal group

        env = kernel.run_function(app__env__get, {'app-dir': app_dir}).first()
        user = user or get_user_or_sudo_user()
        group = group or get_user_group_name(user)
        name = manager.get_config('global.name')

        manager.log(f'Using user {user}:{group}')

        # Get a full config copy
        runtime_config = manager.config.copy()
        # Add the per-environment config.
        runtime_config.update(manager.config['env'][env])

        domains = []
        if 'domains' in runtime_config:
            domains = runtime_config['domains']

        if 'domain_main' in runtime_config and runtime_config['domain_main'] not in domains:
            domains.append(runtime_config['domain_main'])

        # Add extra runtime config.
        runtime_config.update({
            'domains': domains,
            'domains_string': ','.join(domains),
            'domain_tld': (runtime_config['domain_tld']
                           if 'domain_tld' in runtime_config
                           else runtime_config['domain_main']),
            'env': env,
            'name': f'{name}_{env}',
            'host': {
                'ip': socket.gethostbyname(
                    socket.gethostname()
                )
            },
            'password': {
                'insecure': PASSWORD_INSECURE
            },
            'path': {
                'app': app_dir,
                'app_wex': os.path.join(app_dir, APP_DIR_APP_DATA) + '/',
                'proxy': manager.proxy_path
            },
            'service': {},
            'started': False,
            'user': {
                'group': group,
                'gid': get_gid_from_group_name(group),
                'name': user,
                'uid': get_uid_from_user_name(user),
            }
        })

        # Build paths to services docker compose yml files.
        for service, service_data in kernel.registry['services'].items():
            base_yml = service_data['dir'] + 'docker/docker-compose.yml'
            env_yml = service_data['dir'] + f'docker/docker-compose.{env}.yml'

            if not os.path.exists(env_yml):
                env_yml = base_yml

            runtime_config['service'][service] = {
                'yml': {
                    'base': base_yml,
                    'env': env_yml,
                }
            }

        manager.log(f'Build config file')

        manager.runtime_config = runtime_config
        manager.save_runtime_config()

        kernel.run_function(
            app__hook__exec,
            {
                'app-dir': app_dir,
                'hook': 'config/runtime'
            }
        )

    def _app__config__write__docker(previous):
        kernel.run_function(
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

        if not len(compose_files) != 0:
            manager.log('No docker compose file')
            return

        manager.log(f'Compiling docker compose file...')
        yml_content = exec_app_docker_compose(
            kernel,
            app_dir,
            compose_files,
            'config'
        )

        print(yml_content)

        with open(os.path.join(
                app_dir,
                APP_FILEPATH_REL_COMPOSE_RUNTIME_YML
        ), 'w') as f:
            f.write(yml_content)

        kernel.run_function(
            app__hook__exec,
            {
                'app-dir': app_dir,
                'hook': 'config/write-post'
            }
        )

    return ResponseCollectionResponse(kernel, [
        _app__config__write__runtime,
        _app__config__write__docker,
    ])

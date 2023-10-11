import os.path
import glob

import yaml

from addons.app.const.app import APP_DIR_APP_DATA
from addons.app.command.service.install import app__service__install
from src.helper.string import to_snake_case
from src.core import Kernel
from addons.app.AppAddonManager import AppAddonManager


def migration_5_0_0(kernel: Kernel, manager: AppAddonManager):
    env_dir = f'{manager.app_dir}{APP_DIR_APP_DATA}'
    # Convert main config file.
    config = _parse_4_0_0_config_file(f'{env_dir}config')
    if config:
        for domain_env_name in ['LOCAL', 'DEV', 'PROD']:
            env_name = domain_env_name.lower()
            manager.config['env'][env_name]['domains'] = sorted(
                _get_config_value(config, domain_env_name + '_DOMAINS', []))
            manager.config['env'][env_name]['domain_main'] = _get_config_value(config, domain_env_name + '_DOMAIN_MAIN')

            manager.config['env'][env_name]['email'] = _get_config_value(config, domain_env_name + '_EMAIL',
                                                                         'contact@domain.com')
        # Global
        manager.config['global']['name'] = _get_config_value(config, 'NAME',
                                                             manager.get_config('global.config', 'undefined'))

        # Services
        services = _get_config_value(config, 'SERVICES', [])
        for service_name in services:
            kernel.run_function(
                app__service__install,
                {
                    'service': to_snake_case(service_name),
                    'install-docker': False,
                    'install-git': False,
                    'force': True
                }
            )

        # # Database
        # db_container = _get_config_value(config, 'DB_CONTAINER')
        # if db_container:
        #     manager.config['db'] = manager.config['db'] if 'db' in manager.config else {'main': {}}
        #     manager.config['db']['main']['name'] = db_container

        mysql_db_password = _get_config_value(config, 'MYSQL_DB_PASSWORD')
        if mysql_db_password:
            manager.config['service']['mysql_8']['password'] = mysql_db_password

    # Convert docker files.
    docker_dir = f'{env_dir}docker/'

    # Use glob to search for all docker-compose.*.yml files in the specified directory
    docker_files = glob.glob(f"{docker_dir}docker-compose.*")

    replacement_mapping = {
        "APP_ENV": "RUNTIME_ENV",
        "APP_PATH_ROOT": "RUNTIME_PATH_APP",
        "APP_PATH_WEX": "RUNTIME_PATH_APP_WEX",
        "APP_NAME": "GLOBAL_NAME",
        "CONTEXT_ENV": "RUNTIME_ENV",
        "DB_CONTAINER": "DB_MAIN_NAME",
        "DOMAINS": "RUNTIME_DOMAINS_STRING",
        "DOMAIN_MAIN": "RUNTIME_DOMAIN_MAIN",
        "WEX_COMPOSE_YML_MYSQL_8": "RUNTIME_SERVICE_MYSQL_8_YML_ENV",
        "WEX_COMPOSE_YML_LARAVEL_5": "RUNTIME_SERVICE_LARAVEL_5_YML_ENV",
        "WEX_COMPOSE_YML_PHPMYADMIN": "RUNTIME_SERVICE_PHPMYADMIN_YML_ENV",
        "GITLAB_VERSION": _get_config_value(config, 'GITLAB_VERSION', '16.4.1-ce.0'),
        "N8N_VERSION": _get_config_value(config, 'N8N_VERSION'),
        "ROCKETCHAT_VERSION": _get_config_value(config, 'ROCKETCHAT_VERSION'),
        "NEXTCLOUD_VERSION": _get_config_value(config, 'NEXTCLOUD_VERSION'),
        "GRAFANA_VERSION": _get_config_value(config, 'GRAFANA_VERSION', '9.5.12'),
        "JENKINS_VERSION": _get_config_value(config, 'JENKINS_VERSION', '2.60.3-alpine'),
        "MONGO_VERSION": _get_config_value(config, 'MONGO_VERSION'),
        "MATOMO_VERSION": _get_config_value(config, 'MATOMO_VERSION'),
        "ONLYOFFICE_DOCUMENT_SERVER_VERSION": _get_config_value(config, 'ONLYOFFICE_DOCUMENT_SERVER_VERSION'),
        "SONARQUBE_VERSION": _get_config_value(config, 'SONARQUBE_VERSION'),
    }

    # Raw file replacements
    # Loop through each docker-compose file
    for docker_file in docker_files:
        # Read the file content
        with open(docker_file, 'r') as f:
            content = f.read()

        # Replace strings based on the mapping dictionary
        for old_str, new_str in replacement_mapping.items():
            content = content.replace('${' + old_str + '}', '${' + new_str + '}')

        # Override the file with updated content
        with open(docker_file, 'w') as f:
            f.write(content)

    # Yml file changes
    # Loop through each docker-compose file
    for docker_file in docker_files:
        # Read the YAML file
        with open(docker_file, 'r') as f:
            content = yaml.safe_load(f)

        # "version" is no longer required
        if 'version' in content:
            del content['version']

        # Override the YAML file
        with open(docker_file, 'w') as f:
            yaml.dump(content, f)


def is_version_5_0_0(kernel: Kernel, path: str):
    # Not implemented yet.
    return None


def _get_config_value(config: dict, key: str, default=None):
    return config[key] if key in config else default


def _parse_4_0_0_config_file(file_path: str):
    if not os.path.isfile(file_path):
        return None

    config = {}

    with open(file_path, 'r') as f:
        for line in f.readlines():
            # Ignoring comments and empty lines
            line = line.strip()
            if line.startswith("#") or not line:
                continue

            key, value = line.split("=", 1)

            # If the value contains commas, convert it to a list
            if ',' in value:
                value = value.split(',')

            config[key] = value

    return config

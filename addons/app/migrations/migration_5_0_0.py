import os.path
import yaml

from addons.app.const.app import APP_DIR_APP_DATA
from addons.app.command.service.install import app__service__install
from src.helper.prompt import progress_steps
from src.helper.string import to_snake_case
from src.core import Kernel
from addons.app.AppAddonManager import AppAddonManager
from addons.app.migrations.migration_4_0_0 import _migration_4_0_0_replace_docker_placeholders, \
    _migration_4_0_0_et_docker_files


def migration_5_0_0(kernel: Kernel, manager: AppAddonManager):
    env_dir = f'{manager.app_dir}{APP_DIR_APP_DATA}'
    # Convert main config file.
    config = _parse_4_0_0_config_file(f'{env_dir}config')

    services_names_map = {
        'mysql8': 'mysql_8',
        'wordpress5': 'wordpress',
    }

    def _migration_5_0_0_update_config():
        if config:
            for domain_env_name in ['LOCAL', 'DEV', 'PROD']:
                env_name = domain_env_name.lower()
                domains = _get_config_value(config, domain_env_name + '_DOMAINS')

                if domains:
                    manager.config['env'][env_name]['domains'] = sorted(
                        domains.split(',') if isinstance(domains, str) else domains
                    )
                manager.config['env'][env_name]['domain_main'] = _get_config_value(config,
                                                                                   domain_env_name + '_DOMAIN_MAIN')

                manager.config['env'][env_name]['email'] = _get_config_value(config, domain_env_name + '_EMAIL',
                                                                             'contact@domain.com')
            # Global
            manager.config['global']['name'] = _get_config_value(config, 'NAME',
                                                                 manager.get_config('global.config', 'undefined'))

            manager.save_config()

    def _migration_5_0_0_install_services():
        # Services
        services = _get_config_value(config, 'SERVICES', [])
        for service_name in services:
            service_name = services_names_map[service_name] if service_name in services_names_map else service_name

            kernel.run_function(
                app__service__install,
                {
                    'service': to_snake_case(service_name),
                    'install-docker': False,
                    'install-git': False,
                    'force': True
                }
            )

        # Reload config as it may change during services install
        manager.load_config()

    def _migration_5_0_0_config_services():
        # Database (from v3.0.0)
        mysql_db_password = _get_config_value(config, 'MYSQL_PASSWORD')

        if not mysql_db_password:
            mysql_db_password = _get_config_value(config, 'MYSQL_DB_PASSWORD')
        if mysql_db_password:
            manager.config['service']['mysql_8']['password'] = mysql_db_password

    def _migration_5_0_0_update_docker():
        docker_files = _migration_4_0_0_et_docker_files(manager)

        # Yml file changes
        # Loop through each docker-compose file
        for docker_file in docker_files:
            # Read the YAML file
            with open(docker_file, 'r') as f:
                content = yaml.safe_load(f)

            # "version" is no longer required
            if 'version' in content:
                del content['version']

            migration_5_0_0_replace_docker_services_names(content, services_names_map)

            # Override the YAML file
            with open(docker_file, 'w') as f:
                yaml.dump(content, f)

        _migration_4_0_0_replace_docker_placeholders(manager, {
            "APP_ENV": "RUNTIME_ENV",
            "APP_PATH_ROOT": "RUNTIME_PATH_APP",
            "APP_PATH_WEX": "RUNTIME_PATH_APP_WEX",
            "APP_NAME": "GLOBAL_NAME",
            "CONTEXT_ENV": "RUNTIME_ENV",
            "DB_CONTAINER": "DOCKER_MAIN_DB_CONTAINER",
            "DOMAINS": "RUNTIME_DOMAINS_STRING",
            "DOMAIN_MAIN": "RUNTIME_DOMAIN_MAIN",
            "EMAIL": "RUNTIME_EMAIL",
            "WEX_COMPOSE_YML_MYSQL_8": "RUNTIME_SERVICE_MYSQL_8_YML_ENV",
            "WEX_COMPOSE_YML_LARAVEL_5": "RUNTIME_SERVICE_LARAVEL_5_YML_ENV",
            "WEX_COMPOSE_YML_PHPMYADMIN": "RUNTIME_SERVICE_PHPMYADMIN_YML_ENV",
            "WEX_COMPOSE_YML_WORDPRESS5": "RUNTIME_SERVICE_WORDPRESS_YML_ENV",
            'WEX_COMPOSE_YML_MYSQL8': 'RUNTIME_SERVICE_MYSQL_8_YML_ENV',
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
        })

    progress_steps(kernel, [
        _migration_5_0_0_update_config,
        _migration_5_0_0_install_services,
        _migration_5_0_0_config_services,
        _migration_5_0_0_update_docker,
    ])


def migration_5_0_0_replace_docker_services_names(content, services_names_changes):
    if 'services' in content:
        new_services = {}
        for service_name, service_value in content['services'].items():
            new_service_name = service_name
            for search, replacement in services_names_changes.items():
                if search in new_service_name:
                    new_service_name = new_service_name.replace(search, replacement)
            new_services[new_service_name] = service_value

        content['services'] = new_services

    migration_5_0_0_replace_docker_services_references(content, services_names_changes)


def replace_service_names_in_field(field, services_names_changes):
    if isinstance(field, list):
        new_field = []
        for item in field:
            new_item = item
            for search, replacement in services_names_changes.items():
                if search in new_item:
                    new_item = new_item.replace(search, replacement)
            new_field.append(new_item)
        return new_field
    elif isinstance(field, dict):
        new_field = {}
        for key, value in field.items():
            new_key = key
            new_value = value
            for search, replacement in services_names_changes.items():
                if search in new_key:
                    new_key = new_key.replace(search, replacement)
                if isinstance(new_value, str) and search in new_value:
                    new_value = new_value.replace(search, replacement)
            new_field[new_key] = new_value
        return new_field


def migration_5_0_0_replace_docker_services_references(content, services_names_changes):
    if 'services' not in content:
        return

    for service_name, service_value in content['services'].items():
        for field_name in [
            'depends_on',
            'links',
            'extends'
        ]:
            if field_name in service_value:
                service_value[field_name] = replace_service_names_in_field(
                    service_value[field_name],
                    services_names_changes)


def is_version_5_0_0(kernel: Kernel, path: str):
    # Not implemented yet.
    return None


def _get_config_value(config: dict, key: str, default=None):
    return config[key] if key in config else default


def _parse_4_0_0_config_file(file_path: str):
    if not os.path.isfile(file_path):
        return {}

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
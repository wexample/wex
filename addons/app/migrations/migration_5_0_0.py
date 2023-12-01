import os.path
from typing import TYPE_CHECKING, Any, Optional, cast

import yaml

from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.service.install import app__service__install
from addons.app.const.app import APP_DIR_APP_DATA
from addons.app.migrations.migration_4_0_0 import (
    _migration_4_0_0_et_docker_files,
    _migration_4_0_0_replace_docker_mapping,
    _migration_4_0_0_replace_docker_placeholders,
)
from addons.docker.types.docker import DockerCompose
from src.helper.data_yaml import yaml_load
from src.const.types import StringKeysDict, StringsDict, StringsList, AnyList
from src.helper.prompt import prompt_progress_steps
from src.helper.string import string_to_snake_case

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def migration_5_0_0(kernel: "Kernel", manager: AppAddonManager) -> None:
    env_dir = f"{manager.app_dir}{APP_DIR_APP_DATA}"
    # Convert main config file.
    old_config_path = f"{env_dir}config"
    config = _parse_4_0_0_config_file(old_config_path)

    services_names_map: StringsDict = {
        "php8": "php",
        "php_8": "php",
        "php-8": "php",
        "mysql8": "mysql",
        "wordpress5": "wordpress",
    }

    def _migration_5_0_0_update_config() -> None:
        if config:
            for domain_env_name in ["LOCAL", "DEV", "PROD"]:
                env_name = domain_env_name.lower()
                domains = _get_config_value(config, domain_env_name + "_DOMAINS")

                if domains:
                    manager.set_config(
                        f"env.{env_name}.domains",
                        sorted(domains.split(",") if isinstance(domains, str) else domains))

                manager.set_config(
                    f"env.{env_name}.domain_main",
                    _get_config_value(config, domain_env_name + "_DOMAIN_MAIN"))

                manager.set_config(
                    f"env.{env_name}.email",
                    _get_config_value(config, domain_env_name + "_EMAIL", "contact@domain.com"))

            # Global
            manager.set_config(
                "global.name",
                _get_config_value(config, "NAME", manager.get_config("global.config", "undefined")))

            manager.save_config()

    def _migration_5_0_0_install_services() -> None:
        # Services
        services = _get_config_value(config, "SERVICES", [])

        if isinstance(services, str):
            services = [services]

        for service_name in services:
            service_name = (
                services_names_map[service_name]
                if service_name in services_names_map
                else service_name
            )

            kernel.run_function(
                app__service__install,
                {
                    "service": string_to_snake_case(service_name),
                    "install-docker": False,
                    "install-git": False,
                    "force": True,
                },
            )

        # Reload config as it may change during services install
        manager.load_config()

    def _migration_5_0_0_config_services() -> None:
        # Database (from v3.0.0)
        mysql_db_password = _get_config_value(config, "MYSQL_PASSWORD")

        if not mysql_db_password:
            mysql_db_password = _get_config_value(config, "MYSQL_DB_PASSWORD")
        if mysql_db_password:
            manager.set_config(
                "service.mysql.password",
                mysql_db_password)

    def _migration_5_0_0_update_docker() -> None:
        docker_files = _migration_4_0_0_et_docker_files(manager)

        # Yml file changes
        # Loop through each docker-compose file
        for docker_file in docker_files:
            # Read the YAML file
            content = cast(DockerCompose, yaml_load(docker_file))

            # "version" is no longer required
            if "version" in content:
                del content["version"]

            migration_5_0_0_replace_docker_services_names(content, services_names_map)

            # Override the YAML file
            with open(docker_file, "w") as f:
                yaml.dump(content, f)

        _migration_4_0_0_replace_docker_placeholders(
            manager,
            {
                "APP_ENV": "RUNTIME_ENV",
                "APP_PATH_ROOT": "RUNTIME_PATH_APP",
                "APP_PATH_WEX": "RUNTIME_PATH_APP_ENV",
                "APP_NAME": "GLOBAL_NAME",
                "CONTEXT_ENV": "RUNTIME_ENV",
                "DB_CONTAINER": "DOCKER_MAIN_DB_CONTAINER",
                "DOMAINS": "RUNTIME_DOMAINS_STRING",
                "DOMAIN_MAIN": "RUNTIME_DOMAIN_MAIN",
                "EMAIL": "RUNTIME_EMAIL",
                "GITLAB_VERSION": _get_config_value(
                    config, "GITLAB_VERSION", "16.4.1-ce.0"
                ),
                "GRAFANA_VERSION": _get_config_value(
                    config, "GRAFANA_VERSION", "9.5.12"
                ),
                "JENKINS_VERSION": _get_config_value(
                    config, "JENKINS_VERSION", "2.60.3-alpine"
                ),
                "MONGO_VERSION": _get_config_value(config, "MONGO_VERSION"),
                "MATOMO_VERSION": _get_config_value(config, "MATOMO_VERSION"),
                "N8N_VERSION": _get_config_value(config, "N8N_VERSION"),
                "NEXTCLOUD_VERSION": _get_config_value(config, "NEXTCLOUD_VERSION"),
                "ONLYOFFICE_DOCUMENT_SERVER_VERSION": _get_config_value(
                    config, "ONLYOFFICE_DOCUMENT_SERVER_VERSION"
                ),
                "ROCKETCHAT_VERSION": _get_config_value(config, "ROCKETCHAT_VERSION"),
                "SONARQUBE_VERSION": _get_config_value(config, "SONARQUBE_VERSION"),
                "WEX_COMPOSE_YML_MYSQL_8": "RUNTIME_SERVICE_MYSQL_YML_ENV",
                "WEX_COMPOSE_YML_LARAVEL_5": "RUNTIME_SERVICE_LARAVEL_YML_ENV",
                "WEX_COMPOSE_YML_PHP_8": "RUNTIME_SERVICE_PHP_YML_ENV",
                "WEX_COMPOSE_YML_PHPMYADMIN": "RUNTIME_SERVICE_PHPMYADMIN_YML_ENV",
                "WEX_COMPOSE_YML_WORDPRESS5": "RUNTIME_SERVICE_WORDPRESS_YML_ENV",
                "WEX_COMPOSE_YML_MYSQL8": "RUNTIME_SERVICE_MYSQL_YML_ENV",
            },
        )

        _migration_4_0_0_replace_docker_mapping(
            manager,
            {
                # The only cli known was wordpress_cli
                "service: cli": "service: wordpress_cli",
            },
        )

    def _migration_5_0_0_delete_old_files() -> None:
        if os.path.exists(old_config_path):
            os.remove(old_config_path)

    prompt_progress_steps(
        kernel,
        [
            _migration_5_0_0_update_config,
            _migration_5_0_0_install_services,
            _migration_5_0_0_config_services,
            _migration_5_0_0_update_docker,
            _migration_5_0_0_delete_old_files,
        ],
    )


def migration_5_0_0_replace_docker_services_names(
    content: DockerCompose, services_names_changes: StringsDict
) -> None:
    if "services" in content:
        new_services = {}
        for service_name, service_value in content["services"].items():
            assert isinstance(service_value, dict)

            new_service_name = service_name
            for search, replacement in services_names_changes.items():
                if search in new_service_name:
                    new_service_name = new_service_name.replace(search, replacement)
            new_services[new_service_name] = service_value

        content["services"] = new_services

    migration_5_0_0_replace_docker_services_references(content, services_names_changes)


def replace_service_names_in_field(
    field: StringsDict | StringsList, services_names_changes: StringsDict
) -> Optional[StringsDict | StringsList]:
    if isinstance(field, list):
        field_list: AnyList = []
        for item in field:
            new_item = item
            for search, replacement in services_names_changes.items():
                if search in new_item:
                    new_item = new_item.replace(search, replacement)
            field_list.append(new_item)
        return field_list
    elif isinstance(field, dict):
        field_dict: StringKeysDict = {}
        for key, value in field.items():
            new_key = key
            new_value = value
            for search, replacement in services_names_changes.items():
                if search in new_key:
                    new_key = new_key.replace(search, replacement)
                if isinstance(new_value, str) and search in new_value:
                    new_value = new_value.replace(search, replacement)
            field_dict[new_key] = new_value
        return field_dict
    return None


def migration_5_0_0_replace_docker_services_references(
    content: DockerCompose, services_names_changes: StringsDict
) -> None:
    if "services" not in content:
        return

    for service_name, service_value in content["services"].items():
        for field_name in ["depends_on", "links", "extends"]:
            if field_name in service_value:
                service_value_dict = cast(StringKeysDict, service_value)

                service_value_dict[field_name] = replace_service_names_in_field(
                    service_value_dict[field_name], services_names_changes
                )


def is_version_5_0_0(kernel: "Kernel", path: str) -> Optional[bool]:
    # Not implemented yet.
    return None


def _get_config_value(
    config: StringKeysDict, key: str, default: Optional[Any] = None
) -> Any:
    return config[key] if key in config else default


def _parse_4_0_0_config_file(file_path: str) -> StringsDict:
    if not os.path.isfile(file_path):
        return {}

    config: StringKeysDict = {}

    with open(file_path, "r") as f:
        for line in f.readlines():
            # Ignoring comments and empty lines
            line = line.strip()
            if line.startswith("#") or not line:
                continue

            key, value = line.split("=", 1)

            # If the value contains commas, convert it to a list
            if "," in value:
                config[key] = value.split(",")
            else:
                config[key] = value

    return config

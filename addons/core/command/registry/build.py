import click
import os

import yaml
from yaml import SafeLoader

from addons.app.const.app import APP_FILE_APP_SERVICE_CONFIG
from src.helper.registry import scan_commands_groups
from src.decorator.as_sudo import as_sudo
from src.const.globals import FILE_REGISTRY, COMMAND_SEPARATOR_ADDON, COMMAND_CHAR_SERVICE
from src.helper.file import set_user_or_sudo_user_owner


@click.command
@click.pass_obj
@as_sudo
def core__registry__build(kernel):
    kernel.log('Building registry...')
    addons = kernel.addons

    registry = {
        'addons': build_registry_addons(addons, kernel),
        'services': build_registry_services(addons, kernel)
    }

    registry_path = os.path.join(kernel.path["tmp"], FILE_REGISTRY)
    with open(registry_path, 'w') as f:
        yaml.dump(registry, f)

    set_user_or_sudo_user_owner(registry_path)
    kernel.log('Building complete...')

    kernel.load_registry()


def build_registry_addons(addons, kernel):
    addons_dict = {}

    for addon in addons:
        addon_command_path = os.path.join(kernel.path['addons'], addon, 'command')

        if os.path.exists(addon_command_path):
            addons_dict[addon] = {
                'name': addon,
                'commands': scan_commands_groups(
                    addon_command_path,
                    f'{addon}{COMMAND_SEPARATOR_ADDON}'
                )
            }

    return addons_dict


def build_registry_services(addons, kernel):
    services_dict = {}

    for addon in addons:
        services_dir = os.path.join(kernel.path['addons'], addon, 'services')
        if os.path.exists(services_dir):
            for service in os.listdir(services_dir):
                service_path = os.path.join(services_dir, service)
                config_file_path = os.path.join(service_path, APP_FILE_APP_SERVICE_CONFIG)
                commands_path = os.path.join(service_path, 'command')

                services_dict[service] = {
                    'name': service,
                    'commands': scan_commands_groups(
                        commands_path,
                        f'{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}'
                    ),
                    'addon': addon,
                    'dir': service_path + '/',
                    "config": yaml.load(
                        open(config_file_path),
                        SafeLoader
                    ) if os.path.exists(config_file_path) else {
                        'dependencies': []
                    }
                }

    return services_dict

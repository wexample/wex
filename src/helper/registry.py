import json
import os

from addons.app.const.app import APP_FILE_APP_SERVICE_CONFIG
from src.const.globals import COMMAND_CHAR_SERVICE
from src.helper.file import list_subdirectories


def get_commands_groups_names(kernel, addon):
    group_names = set()

    if addon in kernel.registry['addons']:
        for command in kernel.registry['addons'][addon]['commands'].keys():
            group_name = command.split("::")[1].split("/")[0]
            group_names.add(group_name)
    return list(group_names)


def get_all_commands(registry_part):
    output = {}

    for addon, addon_data in registry_part.items():
        for command, command_data in addon_data['commands'].items():
            output[command] = command_data

    return output


def get_all_services_names(kernel):
    output = []

    for service in kernel.registry['services']:
        output.append(kernel.registry['services'][service]['name'])

    return output


def scan_commands(directory, group, prefix, endswith='.py'):
    """Scans the given directory for command files and returns a dictionary of found commands."""
    commands = {}
    for command in os.listdir(directory):
        if command.endswith(endswith):
            command_name, ext = os.path.splitext(command)
            test_file = os.path.realpath(os.path.join(directory, '../../tests/command', group, command))
            commands[f"{prefix}{group}/{command_name}"] = {
                'file': os.path.join(directory, command),
                'test': test_file if os.path.exists(test_file) else None
            }
    return commands


def build_registry_addons(addons, kernel):
    addons_dict = {}

    for addon in addons:
        addon_path = os.path.join(kernel.path['addons'], addon, 'command')
        if os.path.exists(addon_path):
            command_dict = {}
            for group in list_subdirectories(addon_path):
                group_path = os.path.join(addon_path, group)
                command_dict.update(scan_commands(group_path, group, f"{addon}::"))
            addons_dict[addon] = {'name': addon, 'commands': command_dict}

    return addons_dict


def build_registry_services(addons, kernel):
    services_dict = {}

    for addon in addons:
        services_dir = os.path.join(kernel.path['addons'], addon, 'services')
        if os.path.exists(services_dir):
            for service in os.listdir(services_dir):
                service_path = os.path.join(services_dir, service)
                config_file_path = os.path.join(service_path, APP_FILE_APP_SERVICE_CONFIG)
                services_dict[service] = {
                    'name': service,
                    'commands': scan_commands(os.path.join(service_path, 'command'), service, f"{COMMAND_CHAR_SERVICE}"),
                    'addon': addon,
                    'dir': service_path + '/',
                    "config": json.load(open(config_file_path)) if os.path.exists(config_file_path) else {}
                }

    return services_dict
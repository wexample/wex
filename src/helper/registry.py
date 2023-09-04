import os

from src.const.globals import COMMAND_SEPARATOR_ADDON
from src.helper.file import list_subdirectories


def get_all_commands(kernel):
    registry = {}

    for processor in kernel.processors:
        registry = {**registry, **kernel.processors[processor].get_commands_registry(kernel)}

    return registry


def get_all_commands_from_addons(kernel):
    return get_all_commands_from_registry_part(kernel.registry['addons'])


def get_all_commands_from_services(kernel):
    return get_all_commands_from_registry_part(kernel.registry['services'])


def get_commands_groups_names(kernel, addon):
    group_names = set()

    if addon in kernel.registry['addons']:
        for command in get_all_commands_from_addons(kernel).keys():
            group_name = command.split(COMMAND_SEPARATOR_ADDON)[1].split("/")[0]
            group_names.add(group_name)
    return list(group_names)


def get_all_commands_from_registry_part(registry_part: dict) -> dict:
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


def remove_addons(commands_list: []) -> []:
    return [
        command.split(COMMAND_SEPARATOR_ADDON)[1] for command in commands_list
    ]

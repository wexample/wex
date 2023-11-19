from src.const.globals import COMMAND_SEPARATOR_ADDON, COMMAND_TYPE_ADDON
from src.helper.dict import dict_merge


def get_all_commands(kernel) -> dict:
    registry = {}

    for resolver in kernel.resolvers:
        registry = {**registry, **kernel.resolvers[resolver].get_commands_registry()}

    return registry


def get_commands_groups_names(kernel, addon):
    group_names = set()

    if addon in kernel.registry[COMMAND_TYPE_ADDON]:
        for command in kernel.resolvers[COMMAND_TYPE_ADDON].get_commands_registry().keys():
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

    for service in kernel.registry['service']:
        output.append(kernel.registry['service'][service]['name'])

    return output


def remove_addons(commands_list: []) -> []:
    return [
        command.split(COMMAND_SEPARATOR_ADDON)[1] for command in commands_list
    ]


def resolve_service_inheritance(service, services_dict):
    if 'extends' in service['config']:
        parent_name = service['config']['extends']
        if parent_name in services_dict:
            parent_service = services_dict[parent_name]
            resolve_service_inheritance(parent_service, services_dict)
            service['config'] = dict_merge(parent_service['config'], service['config'])
    return service


def find_commands_by_function_property(kernel, name: str) -> dict:
    commands = get_all_commands(kernel)
    filtered = {}

    for command in commands:
        if name in commands[command]['properties']:
            filtered[command] = commands[command]

    return filtered

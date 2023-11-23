from __future__ import annotations
from typing import Dict, Any, List

from src.core.registry.CommandGroup import RegistryCommandGroup
from src.const.globals import COMMAND_SEPARATOR_ADDON, COMMAND_TYPE_ADDON
from src.helper.dict import dict_merge
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel
    from src.const.types import RegistryResolver


def registry_get_all_commands(kernel: 'Kernel') -> Dict[str, Any]:
    registry: Dict[str, Any] = {}

    for resolver in kernel.resolvers:
        registry = {**registry, **kernel.resolvers[resolver].get_commands_registry().commands}

    return registry


def registry_get_all_commands_from_registry_part(
        registry_part: Dict[str, Dict[str, Any]]) -> RegistryCommandGroup:
    output: RegistryCommandGroup = RegistryCommandGroup()

    for addon, addon_data in registry_part.items():
        for command, command_data in addon_data['commands'].items():
            output.commands[command] = command_data

    return output


def registry_remove_addons(commands_list: List[str]) -> List[str]:
    return [
        command.split(COMMAND_SEPARATOR_ADDON)[1] for command in commands_list
    ]


def registry_resolve_service_inheritance(service: Dict[str, Any], services_dict: 'RegistryResolver') -> Dict[str, Any]:
    if 'extends' in service['config']:
        parent_name = service['config']['extends']
        if parent_name in services_dict:
            parent_service = services_dict[parent_name]
            registry_resolve_service_inheritance(parent_service, services_dict)
            service['config'] = dict_merge(parent_service['config'], service['config'])
    return service


def registry_find_commands_by_function_property(kernel: 'Kernel', name: str) -> Dict[str, Any]:
    commands = registry_get_all_commands(kernel)
    filtered = {}

    for command in commands:
        if name in commands[command]['properties']:
            filtered[command] = commands[command]

    return filtered

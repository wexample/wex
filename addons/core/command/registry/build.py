import click
import os
import json
from src.const.globals import FILE_REGISTRY

from src.helper.file import list_subdirectories


@click.command
@click.pass_obj
def core_registry_build(kernel) -> None:
    kernel.log('Building registry...')

    addons = kernel.addons

    registry = {
        'addons': {
            addon: {
                'name': addon,
                'commands': {
                    f"{addon}::{group}/{os.path.splitext(command_name)[0]}": {
                        'file': os.path.join(addon_command_dir, group, command),
                        'test': test_file if os.path.exists(test_file) else None
                    }
                    for group in list_subdirectories(addon_command_dir)
                    for command in os.listdir(os.path.join(addon_command_dir, group))
                    if command.endswith('.py')
                    for command_name, ext in [os.path.splitext(command)]
                    for test_file in [os.path.join(addon_dir, 'tests', 'command', group, command)]
                }
            }
            for addon in addons
            for addon_dir in [os.path.join(kernel.path['addons'], addon)]
            for addon_command_dir in [os.path.join(addon_dir, 'command')]
            if os.path.exists(addon_command_dir)
        },
        'services': {
            service: {
                'name': service,
                'addon': addon,
                "config": json.load(open(service_config_file)) if os.path.exists(service_config_file) else {}
            }
            for addon in addons
            for addon_dir in [os.path.join(kernel.path['addons'], addon)]
            for service_dir in [os.path.join(addon_dir, 'services')]
            if os.path.exists(service_dir)
            for service in os.listdir(service_dir)
            for service_config_file in [os.path.join(service_dir, service, 'service.config.json')]
        }
    }

    with open(f'{kernel.path["tmp"]}{FILE_REGISTRY}', 'w') as f:
        json.dump(registry, f, indent=True)

    kernel.log('Building complete ...')

import click
import os
import json

from addons.app.const.app import APP_FILE_APP_SERVICE_CONFIG
from src.decorator.as_sudo import as_sudo
from src.const.globals import FILE_REGISTRY, COMMAND_CHAR_SERVICE
from src.helper.file import list_subdirectories, set_sudo_user_owner


@click.command
@click.pass_obj
@as_sudo
def core__registry__build(kernel) -> None:
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
                'commands': {
                    f"{COMMAND_CHAR_SERVICE}{service}/{os.path.splitext(command_name)[0]}": {
                        'file': os.path.join(service_command_dir, command),
                        # TODO 'test': test_file if os.path.exists(test_file) else None
                    }
                    for service_command_dir in [os.path.join(service_dir, service, 'command')]
                    if os.path.exists(service_command_dir)
                    for command in os.listdir(service_command_dir)
                    if command.endswith('.py')
                    for command_name, ext in [os.path.splitext(command)]
                },
                'addon': addon,
                'dir': service_dir + '/' + service + '/',
                "config": json.load(open(service_config_file)) if os.path.exists(service_config_file) else {}
            }
            for addon in addons
            for addon_dir in [os.path.join(kernel.path['addons'], addon)]
            for service_dir in [os.path.join(addon_dir, 'services')]
            if os.path.exists(service_dir)
            for service in os.listdir(service_dir)
            for service_config_file in [
                os.path.join(
                    service_dir,
                    service,
                    APP_FILE_APP_SERVICE_CONFIG
                )]
        }
    }

    registry_path = f'{kernel.path["tmp"]}{FILE_REGISTRY}'
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=True)

    set_sudo_user_owner(registry_path)

    kernel.log('Building complete ...')

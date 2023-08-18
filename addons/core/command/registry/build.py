import click
import os
import json

from addons.app.const.app import APP_FILE_APP_SERVICE_CONFIG
from helper.registry import scan_commands
from src.decorator.as_sudo import as_sudo
from src.const.globals import FILE_REGISTRY, COMMAND_CHAR_SERVICE
from src.helper.file import list_subdirectories, set_sudo_user_owner


@click.command
@click.pass_obj
@as_sudo
def core__registry__build(kernel):
    kernel.log('Building registry...')
    addons = kernel.addons
    addons_dict = {}

    for addon in addons:
        if os.path.exists(os.path.join(kernel.path['addons'], addon, 'command')):
            command_dict = {}
            for group in list_subdirectories(os.path.join(kernel.path['addons'], addon, 'command')):
                command_dict.update(scan_commands(
                    os.path.join(kernel.path['addons'], addon, 'command', group),
                    group,
                    f"{addon}::"
                ))
            addons_dict[addon] = {
                'name': addon,
                'commands': command_dict
            }

    registry = {
        'addons': addons_dict,
        'services': {
            service: {
                'name': service,
                'commands': scan_commands(
                    os.path.join(services_dir, service, 'command'),
                    service,
                    f"{COMMAND_CHAR_SERVICE}"
                ),
                'addon': addon,
                'dir': os.path.join(services_dir, service) + '/',
                "config": json.load(
                    open(os.path.join(services_dir, service, APP_FILE_APP_SERVICE_CONFIG))) if os.path.exists(
                    os.path.join(services_dir, service, APP_FILE_APP_SERVICE_CONFIG)) else {}
            }
            for addon in addons
            for addon_dir in [os.path.join(kernel.path['addons'], addon)]
            for services_dir in [os.path.join(addon_dir, 'services')]
            if os.path.exists(services_dir)
            for service in os.listdir(os.path.join(kernel.path['addons'], addon, 'services'))
        }
    }

    registry_path = os.path.join(kernel.path["tmp"], FILE_REGISTRY)
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=4)

    set_sudo_user_owner(registry_path)
    kernel.log('Building complete...')

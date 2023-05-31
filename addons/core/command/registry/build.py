import click
import os
import json

from src.const.globals import FILE_REGISTRY
from src.helper.file import list_subdirectories


@click.command
@click.pass_obj
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
    }

    with open(f'{kernel.path["tmp"]}{FILE_REGISTRY}', 'w') as f:
        json.dump(registry, f, indent=True)

    kernel.log('Building complete ...')

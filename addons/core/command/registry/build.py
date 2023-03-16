import click
import os
import json


@click.command
@click.pass_obj
def core_registry_build(kernel) -> None:
    kernel.log('Building registry...')

    registry = {
        'addons': {
            addon: {
                'name': addon,
                'commands': {
                    f"{addon}::{group}/{os.path.splitext(command_name)[0]}": {
                        'file': os.path.join(addon_dir, group, command),
                        'test': None
                    }
                    for group in kernel.list_subdirectories(os.path.join(addon_dir))
                    for command in os.listdir(os.path.join(addon_dir, group))
                    if command.endswith('.py')
                    for command_name, ext in [
                        os.path.splitext(command)
                    ]
                }
            }
            for addon in kernel.addons
            for addon_dir in [os.path.join(kernel.path['addons'], addon, 'command')]
            if os.path.exists(addon_dir)
        }
    }

    with open(f'{kernel.path["tmp"]}registry.json', 'w') as f:
        json.dump(registry, f, indent=True)

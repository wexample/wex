import click
import os
import json

from src.helper.registry import build_registry_addons, build_registry_services
from src.decorator.as_sudo import as_sudo
from src.const.globals import FILE_REGISTRY
from src.helper.file import set_sudo_user_owner


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
        json.dump(registry, f, indent=4)

    set_sudo_user_owner(registry_path)
    kernel.log('Building complete...')

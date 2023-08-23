from typing import Union, List

import click
from addons.app.decorator.app_location_optional import app_location_optional

from src.helper.args import split_arg_array


@click.command
@click.pass_obj
@app_location_optional
@click.option('--service', '-s', type=str, required=True,
              help="Find all service dependencies")
def core__service__resolve(kernel, service: Union[str, List[str]]) -> List[str]:
    services = split_arg_array(service)

    resolved_services = set()

    def resolve_dependencies(service: str, resolved_services: set):
        if service in resolved_services:
            return set()

        resolved_services.add(service)

        if service in kernel.registry['services']:
            config = kernel.registry['services'][service]['config']
            dependencies = config.get('dependencies', [])

            for dependency in dependencies:
                resolved_services.update(
                    resolve_dependencies(dependency, resolved_services)
                )

        return resolved_services

    for service in services:
        resolve_dependencies(service, resolved_services)

    return list(resolved_services)

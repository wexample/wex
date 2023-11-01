from typing import List

from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option
from src.helper.args import split_arg_array


@command(help="Resolve dependencies of a service")
@option('--service', '-s', required=True,
        help="Find all service dependencies")
def core__service__resolve(kernel: Kernel, service) -> List[str]:
    services = split_arg_array(service)
    resolved_services = set()

    def resolve_dependencies(service: str, resolved_services: set):
        if service in resolved_services:
            return set()

        resolved_services.add(service)

        if service in kernel.registry['service']:
            config = kernel.registry['service'][service]['config']
            dependencies = config.get('dependencies', [])

            for dependency in dependencies:
                resolved_services.update(
                    resolve_dependencies(dependency, resolved_services)
                )

        return resolved_services

    for service in services:
        resolve_dependencies(service, resolved_services)

    return list(resolved_services)

from typing import TYPE_CHECKING, Set

from src.const.globals import COMMAND_TYPE_SERVICE
from src.const.types import CoreCommandCommaSeparatedList, SetList, StringsList
from src.decorator.command import command
from src.decorator.option import option
from src.helper.args import args_split_arg_array

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Resolve dependencies of a service")
@option("--service", "-s", required=True, help="Find all service dependencies")
def core__service__resolve(
    kernel: "Kernel", service: CoreCommandCommaSeparatedList
) -> StringsList:
    services = args_split_arg_array(service)
    resolved_services: StringsList = []

    def resolve_dependencies(service: str, resolved_services: StringsList) -> None:
        if service in resolved_services:
            return

        resolved_services.append(service)

        services_registry = kernel.resolvers[COMMAND_TYPE_SERVICE].get_registry_data()
        if service in services_registry:
            config = services_registry[service]["config"]
            dependencies = config.get("dependencies", [])

            for dependency in dependencies:
                resolve_dependencies(dependency, resolved_services)

    for service in services:
        resolve_dependencies(service, resolved_services)

    return resolved_services

import os
from typing import TYPE_CHECKING, Optional, cast

from addons.app.const.app import APP_FILE_APP_SERVICE_CONFIG, ERR_SERVICE_NOT_FOUND
from src.const.globals import (
    COMMAND_CHAR_SERVICE,
    COMMAND_PATTERN_SERVICE,
    COMMAND_SEPARATOR_ADDON,
    COMMAND_TYPE_SERVICE,
)
from src.const.typing import (
    AnyCallable,
    RegistryAllServices,
    RegistryService,
    StringsList,
)
from src.core.command.resolver.AbstractCommandResolver import AbstractCommandResolver
from src.core.CommandRequest import CommandRequest
from src.core.response.AbortResponse import AbortResponse
from src.helper.data_yaml import yaml_load
from src.helper.service import service_get_dir
from src.helper.string import string_to_snake_case

if TYPE_CHECKING:
    from src.core.response.AbstractResponse import AbstractResponse


class ServiceCommandResolver(AbstractCommandResolver):
    def render_request(
        self, request: CommandRequest, render_mode: str
    ) -> "AbstractResponse":
        match = request.get_match()
        service = string_to_snake_case(match[1]) if match else None
        if not service or service not in self.get_registry_data():
            if not request.quiet:
                self.kernel.io.error(
                    ERR_SERVICE_NOT_FOUND,
                    {
                        "command": request.get_string_command(),
                        "service": str(service),
                    },
                )
            return AbortResponse(self.kernel, reason=ERR_SERVICE_NOT_FOUND)

        # Guess service name from command prefix if not passed.
        args_list = request.get_args_list()
        if "--service" not in args_list:
            args_list.extend(["--service", service])

        return super().render_request(request, render_mode)

    @classmethod
    def get_pattern(cls) -> str:
        return COMMAND_PATTERN_SERVICE

    @classmethod
    def get_type(cls) -> str:
        return COMMAND_TYPE_SERVICE

    def build_command_from_parts(self, parts: StringsList) -> str:
        return COMMAND_CHAR_SERVICE + super().build_command_from_parts(parts)

    def build_path(
        self, request: CommandRequest, extension: str, subdir: Optional[str] = None
    ) -> Optional[str]:
        match = request.get_match()
        name = string_to_snake_case(match[1])
        path = service_get_dir(self.kernel, name)

        if not path:
            self.kernel.io.error(f"Service not found : {name}")

        return self.build_command_path(
            base_path=str(path),
            extension=extension,
            subdir=subdir,
            command_path=os.path.join(
                string_to_snake_case(match.group(2)),
                string_to_snake_case(match.group(3)),
            ),
        )

    def get_function_name_parts(self, parts: StringsList) -> StringsList:
        return [parts[0], parts[1], parts[2]]

    def autocomplete_suggest(
        self, cursor: int, search_split: StringsList
    ) -> str | None:
        # Suggest @
        if cursor == 0 and search_split[0] == "":
            return COMMAND_CHAR_SERVICE

        # In every other case, search should start with @
        if search_split[0] == COMMAND_CHAR_SERVICE:
            if cursor <= 1:
                if search_split[0] == COMMAND_CHAR_SERVICE:
                    commands = [
                        command
                        for command in self.get_commands_registry().keys()
                        if command.startswith("".join(search_split))
                    ]

                    return " ".join(commands)

                elif search_split[0] == "":
                    return COMMAND_CHAR_SERVICE
            elif cursor == 2 or cursor == 3:
                if search_split[2] == COMMAND_SEPARATOR_ADDON:
                    search_service = "".join(search_split[:3])
                    search = "".join(search_split)

                    commands = [
                        command[len(search_service) :]
                        for command in self.get_commands_registry().keys()
                        if command.startswith(search)
                    ]

                    return " ".join(commands)
                elif cursor == 2 and search_split[2] == ":":
                    # User types "core:", we add a second ":"
                    return ":"
            # Arguments
            elif cursor >= 4:
                return self.suggest_arguments(
                    "".join(search_split[0:4]),
                    search_split[cursor],
                )

        return None

    def locate_function(self, request: CommandRequest) -> bool:
        """
        Support services inheritance, if a function is not found in a service,
        search it into parent service.
        """
        from src.helper.service import service_get_inheritance_tree

        request.match = self.build_match(request.get_string_command())

        if request.match:
            tree = service_get_inheritance_tree(
                self.kernel, string_to_snake_case(request.match[1])
            )

            match_base = request.match
            for service_tree_item in tree:
                request.set_string_command(
                    self.build_command_from_parts(
                        [
                            service_tree_item,
                            request.match[2],
                            request.match[3],
                        ]
                    )
                )

                if super().locate_function(request):
                    request.match = match_base
                    return True

        return False

    @classmethod
    def decorate_command(cls, function: AnyCallable) -> AnyCallable:
        from addons.app.decorator.service_option import service_option

        return cast(AnyCallable, service_option()(function))

    def build_command_parts_from_url_path_parts(
        self, path_parts: StringsList
    ) -> StringsList:
        return [
            path_parts[0],
            path_parts[1],
            path_parts[2],
        ]

    def build_registry_data(self, test: bool = False) -> RegistryAllServices:
        from src.helper.registry import registry_resolve_service_inheritance

        registry: RegistryAllServices = {}

        for addon in self.kernel.addons:
            services_dir = self.kernel.get_path("addons", [addon, "services"])
            if os.path.exists(services_dir):
                for service in os.listdir(services_dir):
                    self.kernel.io.log(f"Found service {service}")
                    service_path = os.path.join(services_dir, service) + os.sep
                    config_file_path = os.path.join(
                        service_path, APP_FILE_APP_SERVICE_CONFIG
                    )
                    commands_path = os.path.join(service_path, "command")

                    registry[service] = cast(
                        RegistryService,
                        {
                            "name": service,
                            "commands": self.scan_commands_groups(commands_path, test),
                            "addon": addon,
                            "dir": service_path,
                            "config": yaml_load(
                                file_path=config_file_path, default={"dependencies": []}
                            ),
                        },
                    )

        # Resolve inheritance
        for service_name, service_data in registry.items():
            registry_resolve_service_inheritance(service_data, registry)

        return registry

    def get_registered_services(self) -> StringsList:
        return cast(StringsList, self.get_registry_data().keys())

    def get_registered_service_data(self, name: str) -> RegistryService:
        return cast(RegistryService, self.get_registry_data()[name])

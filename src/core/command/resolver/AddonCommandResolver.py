import os
from typing import Optional, cast

from src.const.globals import (
    COMMAND_PATTERN_ADDON,
    COMMAND_SEPARATOR_ADDON,
    COMMAND_SEPARATOR_GROUP,
    COMMAND_TYPE_ADDON,
)
from src.const.types import RegistryAddon, RegistryResolverData, StringsList
from src.core.command.resolver.AbstractCommandResolver import AbstractCommandResolver
from src.core.CommandRequest import CommandRequest
from src.helper.registry import registry_get_all_commands
from src.helper.string import string_to_snake_case


class AddonCommandResolver(AbstractCommandResolver):
    @classmethod
    def get_pattern(cls) -> str:
        return COMMAND_PATTERN_ADDON

    @classmethod
    def get_type(cls) -> str:
        return COMMAND_TYPE_ADDON

    def build_path(
        self, request: CommandRequest, extension: str, subdir: Optional[str] = None
    ) -> Optional[str]:
        # Unable to find command path if no addon name found.
        if request.match.group(1) is None:
            return None

        return self.build_command_path(
            base_path=self.kernel.get_path(
                "addons", [string_to_snake_case(request.match.group(1))]
            ),
            extension=extension,
            subdir=subdir,
            command_path=os.path.join(
                string_to_snake_case(request.match.group(2)),
                string_to_snake_case(request.match.group(3)),
            ),
        )

    def get_function_name_parts(self, parts: list) -> []:
        return [
            parts[0],
            parts[1],
            parts[2],
        ]

    def get_function_aliases(self, function) -> list:
        aliases = super().get_function_aliases(function)

        parts = self.build_match(self.build_command_from_function(function)).groups()

        aliases.append(COMMAND_SEPARATOR_GROUP.join([parts[1], parts[2]]))

        return aliases

    def autocomplete_suggest(
        self, cursor: int, search_split: StringsList
    ) -> str | None:
        if cursor == 0:
            # User typed "wex co"
            if search_split[0] != "":
                addons = self.get_registry_data()
                commands_suggestions: StringsList = list(addons.keys())
                # Add separator
                commands_suggestions = [
                    addon + COMMAND_SEPARATOR_ADDON for addon in commands_suggestions
                ]

                for addon in addons:
                    addon_data: RegistryAddon = cast(RegistryAddon, addons[addon])
                    for command in addon_data["commands"]:
                        command_data = addon_data["commands"][command]
                        commands_suggestions += command_data["alias"]

                # Filter
                suggestion = " ".join(
                    [
                        addon
                        for addon in commands_suggestions
                        if addon.startswith(search_split[0])
                    ]
                )

                # If only one result, autocomplete
                return self.suggest_autocomplete_if_single(suggestion)
            # User typed "wex ", we suggest all addons names and special chars.
            else:
                return " ".join(
                    addon + COMMAND_SEPARATOR_ADDON
                    for addon in self.get_registry_data().keys()
                )

        elif cursor == 1:
            registry_data = self.get_registry_data()

            # User typed "wex core::", we suggest all addon groups.
            if search_split[1] == COMMAND_SEPARATOR_ADDON:
                key = search_split[0]
                if key in registry_data and isinstance(registry_data[key], dict):
                    commands_dict = registry_data[key]
                    assert isinstance(commands_dict, dict)
                    commands = commands_dict.get("commands", [])
                    return " ".join(
                        [
                            command[len(key + COMMAND_SEPARATOR_ADDON) :]
                            for command in commands
                            if command.startswith(key + COMMAND_SEPARATOR_ADDON)
                        ]
                    )
                return ""
            elif search_split[1] == ":":
                # User typed "core:", we add a second ":"
                return ":"
        elif cursor == 2:
            from src.helper.registry import (
                registry_get_all_commands,
                registry_remove_addons,
            )

            addon = search_split[0]

            # Get all matching commands
            all_commands = [
                command
                for command in registry_get_all_commands(self.kernel)
                if command.startswith(addon + COMMAND_SEPARATOR_ADDON + search_split[2])
            ]

            suggestion = " ".join(registry_remove_addons(all_commands))

            return self.suggest_autocomplete_if_single(suggestion)

            # Complete arguments.
        elif cursor >= 3:
            from src.helper.registry import registry_get_all_commands

            # Command validity is checked inside
            return self.suggest_arguments(
                "".join(search_split[0:3]),
                search_split[cursor],
            )

        return None

    def suggest_autocomplete_if_single(self, search_string: str) -> str:
        all_commands = registry_get_all_commands(self.kernel)
        all_names = [name for name in all_commands if name.startswith(search_string)]

        if len(all_names) == 1:
            # Adding a trailing space indicates
            # that command is found
            return all_names[0] + " "

        return search_string

    def build_command_parts_from_url_path_parts(
        self, path_parts: StringsList
    ) -> StringsList:
        return [
            path_parts[0],
            path_parts[1],
            path_parts[2],
        ]

    def build_registry_data(self, test: bool = False) -> "RegistryResolverData":
        registry: "RegistryResolverData" = {}

        for addon in self.kernel.addons:
            addon_command_path = self.kernel.get_path("addons", [addon, "command"])

            if os.path.exists(addon_command_path):
                registry[addon] = {
                    "name": addon,
                    "commands": self.scan_commands_groups(addon_command_path, test),
                }

        return registry

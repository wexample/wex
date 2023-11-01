import os

from src.core.CommandRequest import CommandRequest
from src.helper.string import to_snake_case
from src.const.globals import COMMAND_PATTERN_ADDON, COMMAND_TYPE_ADDON, COMMAND_SEPARATOR_ADDON, \
    COMMAND_SEPARATOR_GROUP
from src.core.command.AbstractCommandResolver import AbstractCommandResolver


class AddonCommandResolver(AbstractCommandResolver):

    @classmethod
    def get_pattern(cls) -> str:
        return COMMAND_PATTERN_ADDON

    @classmethod
    def get_type(cls) -> str:
        return COMMAND_TYPE_ADDON

    def build_path(self, request: CommandRequest, subdir: str = None) -> str | None:
        # Unable to find command path if no addon name found.
        if request.match.group(1) is None:
            return None

        return self.build_command_path(
            f"{self.kernel.get_path('addons')}{to_snake_case(request.match.group(1))}/",
            subdir,
            os.path.join(to_snake_case(request.match.group(2)), to_snake_case(request.match.group(3)))
        )

    def get_function_name_parts(self, parts: list) -> []:
        return [
            parts[0],
            parts[1],
            parts[2],
        ]

    def build_alias(self, function, alias: bool | str) -> str:
        if alias == 'NO_ADDON_ALIAS':
            parts = self.build_match(
                self.build_command_from_function(function)
            ).groups()

            return COMMAND_SEPARATOR_GROUP.join([
                parts[1],
                parts[2]
            ])

        return super().build_alias(function, alias)

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        if cursor == 0:
            # User typed "co"
            if search_split[0] != '':
                suggestion = ' '.join(
                    [addon + COMMAND_SEPARATOR_ADDON for addon in self.kernel.registry['addon'].keys() if
                     addon.startswith(search_split[0])])

                # If only one result, autocomplete
                from src.helper.suggest import suggest_autocomplete_if_single
                return suggest_autocomplete_if_single(self.kernel, suggestion)
            # User typed "wex ", we suggest all addons names and special chars.
            else:
                return ' '.join(addon + COMMAND_SEPARATOR_ADDON for addon in self.kernel.registry['addon'].keys())

        elif cursor == 1:
            # User typed "wex core::", we suggest all addon groups.
            if search_split[1] == COMMAND_SEPARATOR_ADDON:
                if search_split[0] in self.kernel.registry['addon']:
                    return ' '.join([
                        command[len(search_split[0] + COMMAND_SEPARATOR_ADDON):]
                        for command in self.kernel.registry['addon'][search_split[0]]['commands']
                        if command.startswith(search_split[0] + COMMAND_SEPARATOR_ADDON)
                    ])
            elif search_split[1] == ':':
                # User types "core:", we add a second ":"
                return ':'
        elif cursor == 2:
            from src.helper.registry import get_all_commands, remove_addons
            addon = search_split[0]

            # Get all matching commands
            all_commands = [command for command in get_all_commands(self.kernel) if command.startswith(
                addon + COMMAND_SEPARATOR_ADDON + search_split[2]
            )]

            suggestion = ' '.join(remove_addons(all_commands))

            from src.helper.suggest import suggest_autocomplete_if_single
            return suggest_autocomplete_if_single(self.kernel, suggestion)

            # Complete arguments.
        elif cursor >= 3:
            from src.helper.registry import get_all_commands

            # Command validity is checked inside
            return self.suggest_arguments(
                ''.join(search_split[0:3]),
                search_split[3:],
            )

        return None

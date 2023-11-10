import os

from src.helper.registry import get_all_commands
from src.core.CommandRequest import CommandRequest
from src.helper.string import to_snake_case
from src.const.globals import COMMAND_PATTERN_ADDON, COMMAND_TYPE_ADDON, COMMAND_SEPARATOR_ADDON, \
    COMMAND_SEPARATOR_GROUP
from src.core.command.resolver.AbstractCommandResolver import AbstractCommandResolver


class AddonCommandResolver(AbstractCommandResolver):

    @classmethod
    def get_pattern(cls) -> str:
        return COMMAND_PATTERN_ADDON

    @classmethod
    def get_type(cls) -> str:
        return COMMAND_TYPE_ADDON

    def build_path(self, request: CommandRequest, extension: str, subdir: str = None) -> str | None:
        # Unable to find command path if no addon name found.
        if request.match.group(1) is None:
            return None

        return self.build_command_path(
            base_path=self.kernel.get_path('addons', [to_snake_case(request.match.group(1))]),
            extension=extension,
            subdir=subdir,
            command_path=os.path.join(to_snake_case(request.match.group(2)), to_snake_case(request.match.group(3)))
        )

    def get_function_name_parts(self, parts: list) -> []:
        return [
            parts[0],
            parts[1],
            parts[2],
        ]

    def get_function_aliases(self, function) -> list:
        aliases = super().get_function_aliases(function)

        parts = self.build_match(
            self.build_command_from_function(function)
        ).groups()

        aliases.append(
            COMMAND_SEPARATOR_GROUP.join([
                parts[1],
                parts[2]
            ])
        )

        return aliases

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        if cursor == 0:
            # User typed "wex co"
            if search_split[0] != '':
                addons = self.kernel.registry['addon']
                commands_suggestions: list = list(addons.keys())
                # Add separator
                commands_suggestions = [addon + COMMAND_SEPARATOR_ADDON for addon in commands_suggestions]

                for addon in addons:
                    for command in addons[addon]['commands']:
                        commands_suggestions += addons[addon]['commands'][command]['alias']

                # Filter
                suggestion = ' '.join(
                    [addon for addon in commands_suggestions if addon.startswith(search_split[0])]
                )

                # If only one result, autocomplete
                return self.suggest_autocomplete_if_single(suggestion)
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
                # User typed "core:", we add a second ":"
                return ':'
        elif cursor == 2:
            from src.helper.registry import get_all_commands, remove_addons
            addon = search_split[0]

            # Get all matching commands
            all_commands = [command for command in get_all_commands(self.kernel) if command.startswith(
                addon + COMMAND_SEPARATOR_ADDON + search_split[2]
            )]

            suggestion = ' '.join(remove_addons(all_commands))

            return self.suggest_autocomplete_if_single(suggestion)

            # Complete arguments.
        elif cursor >= 3:
            from src.helper.registry import get_all_commands

            # Command validity is checked inside
            return self.suggest_arguments(
                ''.join(search_split[0:3]),
                search_split[3:],
            )

        return None

    def suggest_autocomplete_if_single(self, search_string):
        all_commands = get_all_commands(self.kernel)

        all_commands = [
            name for name in all_commands if name.startswith(search_string)
        ]

        if len(all_commands) == 1:
            # Adding a trailing space indicates
            # that command is found
            return all_commands[0] + ' '

        return search_string

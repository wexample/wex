import os

from src.helper.string import to_snake_case
from src.helper.registry import get_all_commands_from_addons
from src.helper.args import convert_dict_to_args
from src.const.globals import COMMAND_PATTERN_ADDON, COMMAND_TYPE_ADDON, COMMAND_SEPARATOR_FUNCTION_PARTS, \
    COMMAND_SEPARATOR_ADDON, COMMAND_SEPARATOR_GROUP, CORE_COMMAND_NAME
from src.core.command.AbstractCommandProcessor import AbstractCommandProcessor


class AddonCommandProcessor(AbstractCommandProcessor):

    @classmethod
    def get_pattern(cls) -> str:
        return COMMAND_PATTERN_ADDON

    @classmethod
    def get_type(cls) -> str:
        return COMMAND_TYPE_ADDON

    def get_path(self, subdir: str = None) -> str | None:
        # Unable to find command path if no addon name found.
        if self.match.group(1) is None:
            return None

        return self.build_command_path(
            f"{self.kernel.path['addons']}{to_snake_case(self.match.group(1))}/",
            subdir,
            os.path.join(to_snake_case(self.match.group(2)), to_snake_case(self.match.group(3)))
        )

    def get_function_name_parts(self) -> []:
        return [
            self.match.group(1),
            self.match.group(2),
            self.match.group(3),
        ]

    @staticmethod
    def get_commands_registry(kernel) -> dict:
        return get_all_commands_from_addons(kernel)

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        # Performance optimisation
        from src.const.globals import COMMAND_SEPARATOR_ADDON

        if cursor == 0:
            # User typed "co"
            if search_split[0] != '':
                suggestion = ' '.join(
                    [addon + COMMAND_SEPARATOR_ADDON for addon in self.kernel.registry['addons'].keys() if
                     addon.startswith(search_split[0])])

                # If only one result, autocomplete
                from src.helper.suggest import suggest_autocomplete_if_single
                return suggest_autocomplete_if_single(self.kernel, suggestion)
            # User typed "wex ", we suggest all addons names and special chars.
            else:
                return ' '.join(addon + COMMAND_SEPARATOR_ADDON for addon in self.kernel.registry['addons'].keys())

        elif cursor == 1:
            # User typed "wex core::", we suggest all addon groups.
            if search_split[1] == COMMAND_SEPARATOR_ADDON:
                if search_split[0] in self.kernel.registry['addons']:
                    return ' '.join([
                        command[len(search_split[0] + COMMAND_SEPARATOR_ADDON):]
                        for command in self.kernel.registry['addons'][search_split[0]]['commands']
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

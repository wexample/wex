import os

from src.helper.registry import get_all_commands_from_addons
from src.helper.args import convert_dict_to_args
from src.const.globals import COMMAND_PATTERN_ADDON, COMMAND_TYPE_ADDON, COMMAND_SEPARATOR_FUNCTION_PARTS, \
    COMMAND_SEPARATOR_ADDON, COMMAND_SEPARATOR_GROUP, CORE_COMMAND_NAME
from src.core.command.AbstractCommandProcessor import AbstractCommandProcessor


class AddonCommandProcessor(AbstractCommandProcessor):

    def get_pattern(self) -> str:
        return COMMAND_PATTERN_ADDON

    def get_type(self) -> str:
        return COMMAND_TYPE_ADDON

    def get_path(self, subdir: str = None) -> str | None:
        # Unable to find command path if no addon name found.
        if self.match.group(1) is None:
            return None

        return self.build_command_path(
            f"{self.kernel.path['addons']}{self.match.group(1)}/",
            subdir,
            os.path.join(self.match.group(2), self.match.group(3))
        )

    def get_function_name(self):
        return COMMAND_SEPARATOR_FUNCTION_PARTS.join([
            self.match.group(1),
            self.match.group(2),
            self.match.group(3),
        ])

    def build_command_parts(self, function_name):
        return function_name.split(COMMAND_SEPARATOR_FUNCTION_PARTS)[:3]

    def build_command_from_function(self, function) -> str | None:
        # Check if parent class returns something
        output = super().build_command_from_function(function)
        if output is not None:
            return output

        parts = self.build_command_parts(function.callback.__name__)

        return f'{parts[0]}{COMMAND_SEPARATOR_ADDON}{parts[1]}{COMMAND_SEPARATOR_GROUP}{parts[2]}'

    def build_full_command_from_function(self, function, args: dict = {}) -> str | None:
        # Check if parent class returns something
        output = super().build_full_command_from_function(function, args)
        if output is not None:
            return output

        output = f'{CORE_COMMAND_NAME} '
        output += self.build_command_from_function(function)

        if len(args):
            output += ' '.join(convert_dict_to_args(function, args))

        return output

    @staticmethod
    def get_commands_registry(kernel) -> dict:
        return get_all_commands_from_addons(kernel)

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        # Performance optimisation
        from src.helper.registry import get_all_commands, remove_addons
        from src.const.globals import COMMAND_SEPARATOR_ADDON, COMMAND_CHAR_SERVICE, COMMAND_CHAR_USER, COMMAND_CHAR_APP

        if cursor == 0:
            # User typed "co"
            if search_split[0] != '':
                suggestion = ' '.join([addon + COMMAND_SEPARATOR_ADDON for addon in self.kernel.registry['addons'].keys() if
                                       addon.startswith(search_split[0])])

                # If only one result, autocomplete
                from src.helper.suggest import suggest_autocomplete_if_single
                return suggest_autocomplete_if_single(self.kernel, suggestion)
            # User typed "wex ", we suggest all addons names and special chars.
            else:
                suggestion = ' '.join(addon + COMMAND_SEPARATOR_ADDON for addon in self.kernel.registry['addons'].keys())
                # Adds also all core actions.
                suggestion += ' ' + ' '.join(self.kernel.get_core_actions().keys())

                return suggestion

        elif cursor == 1:
            # # User typed "wex @x" so we can suggest service names.
            # if search_split[0] == COMMAND_CHAR_SERVICE:
            #     pass
            # #         if COMMAND_SEPARATOR_GROUP in search_split[1]:
            # #             split = search_split[1].split('/', 1)
            # #             service_name = split[0]
            # #
            # #             if service_name in self.kernel.registry['services']:
            # #                 from src.helper.registry import get_all_commands
            # #                 commands = get_all_commands_from_registry_part({service_name: self.kernel.registry['services'][service_name]})
            # #
            # #                 return ' '.join(commands)
            # #         else:
            # #             from src.helper.suggest import get_all_services_names_suggestions
            # #
            # #             suggestion = get_all_services_names_suggestions(self.kernel)
            # #             # If there's only one suggestion (no space separator), add a trailing "/" at the end
            # #             if ' ' not in suggestion:
            # #                 suggestion += COMMAND_SEPARATOR_GROUP

            # User typed "wex core::", we suggest all addon groups.
            if search_split[1] == COMMAND_SEPARATOR_ADDON:
                from src.helper.registry import get_commands_groups_names
                return ' '.join(get_commands_groups_names(self.kernel, search_split[0]))
            elif search_split[1] == ':':
                # User types "core:", we add a second ":"
                return ':'
        elif cursor == 2:
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
            self.set_command(
                ''.join(search_split[0:3])
            )

            params_current = [val for val in search_split[3:] if val.startswith("-")]

            # Merge all params in a list,
            # but ignore already given args,
            # i.e : if -d is already given, do not suggest "-d" or "--default"
            function = self.get_function(self)
            params = []
            for param in function.params:
                if any(opt in params_current for opt in param.opts):
                    continue
                params += param.opts

            return ' '.join(params)

        return None
import re
import click

from src.const.globals import COMMAND_PATTERN
from src.const.globals import COMMAND_SEPARATOR_ADDON, COMMAND_SEPARATOR_GROUP


@click.command
@click.pass_obj
@click.option('--cursor', '-c', type=int, required=True, help="Indicates which part of search string is focused")
@click.option('--search', '-s', type=str, required=True, help="Separated arguments, without first command, i.e. : "
                                                              "app :: config/write")
def core_autocomplete_suggest(kernel, cursor: int, search: str) -> str:
    """
    Works and interact with cli/autocomplete bash command to provide a smart autocomplete intergration.
    Returns a string with suggestions to transmit to bash compgen.
    """
    suggestion = ''

    search_split = search.split(' ')

    # Mismatch between parts and cursor index.
    if cursor > len(search_split):
        return

    search_part = search_split[cursor]

    if cursor == 0:
        # User typed ony "wex ", we suggest all addons names.
        suggestion = ' '.join(kernel.registry['addons'].keys())
    elif cursor == 1:
        # User typed "app::", we suggest all addon groups.
        if search_split[1] == COMMAND_SEPARATOR_ADDON:
            suggestion = ' '.join(kernel.get_group_names(search_split[0]))
        else:
            # User types "app:", we add a second ":"
            suggestion = ':'
    elif cursor == 2:
        addon = search_split[0]

        if addon in kernel.registry['addons']:
            # User typed "wex app::conf", we suggest full addon commands list.
            for command, command_data in kernel.registry['addons'][addon]['commands'].items():
                command_parts = command.split(COMMAND_SEPARATOR_ADDON)
                command_split = command_parts[1].split(COMMAND_SEPARATOR_GROUP)

                if COMMAND_SEPARATOR_GROUP in search_part:
                    if command_split[0] == search_split[2].split(COMMAND_SEPARATOR_GROUP)[0]:
                        suggestion += f' {" ".join(command_parts)}'
                else:
                    suggestion += f' {command_split[0]}'

            # Reduce unique values
            suggestion = " ".join(set(suggestion.split()))
    # Complete arguments.
    elif cursor >= 3:
        command = search_split[0:3]
        params_current = [val for val in search_split[3:] if val.startswith("-")]

        match = re.match(
            COMMAND_PATTERN,
            ''.join(command)
        )

        if not match:
            return

        # Merge all params in a list,
        # but ignore already given args,
        # i.e : if -d is already given, do not suggest "-d" or "--default"
        function = kernel.get_function_from_match(match)
        params = []
        for param in function.params:
            if any(opt in params_current for opt in param.opts):
                continue
            params += param.opts

        suggestion = ' '.join(params)

    return suggestion

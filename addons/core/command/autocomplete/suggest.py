import click

from src.helper.registry import get_all_commands, remove_addons
from src.const.globals import COMMAND_SEPARATOR_ADDON, COMMAND_SEPARATOR_GROUP, COMMAND_CHAR_APP, COMMAND_CHAR_SERVICE, \
    COMMAND_CHAR_USER


@click.command
@click.pass_obj
@click.option('--cursor', '-c', type=int, required=True, help="Indicates which part of search string is focused")
@click.option('--search', '-s', type=str, required=True, help="Separated arguments, without first command, i.e. : "
                                                              "app :: config/write")
def core__autocomplete__suggest(kernel, cursor: int, search: str) -> str:
    """
    Works and interact with cli/autocomplete bash command to provide a smart autocomplete integration.
    Returns a string with suggestions to transmit to bash compgen.
    """
    search_split = search.split(' ')

    # Mismatch between parts and cursor index.
    if cursor > len(search_split):
        return ''

    for name in kernel.processors:
        processor = kernel.processors[name](kernel)
        suggestion = processor.autocomplete_suggest(cursor, search_split)

        if suggestion is not None:
            return suggestion

    print('ERR')
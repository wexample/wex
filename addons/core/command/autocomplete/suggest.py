from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option


@command(help="Return suggestion for autocomplete search")
@option('--cursor', '-c', type=int, required=True, help="Indicates which part of search string is focused")
@option('--search', '-s', type=str, required=True, help="Separated arguments, without first command, i.e. : "
                                                        "app :: config/write")
def core__autocomplete__suggest(kernel: Kernel, cursor: int, search: str) -> str:
    """
    Works and interact with cli/autocomplete bash command to provide a smart autocomplete integration.
    Returns a string with suggestions to transmit to bash compgen.
    """
    search_split = search.split(' ')

    # Mismatch between parts and cursor index.
    if cursor > len(search_split):
        return ''

    suggestions = ''
    for name in kernel.resolvers:
        resolver = kernel.resolvers[name](kernel)
        new_suggestions = resolver.autocomplete_suggest(cursor, search_split)

        if new_suggestions is not None:
            suggestions += ' ' + new_suggestions

    return suggestions.strip()

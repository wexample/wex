import click


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

    suggestions = ''
    for name in kernel.processors:
        processor = kernel.processors[name](kernel)
        new_suggestions = processor.autocomplete_suggest(cursor, search_split)

        if new_suggestions is not None:
            suggestions += ' ' + new_suggestions

    return suggestions.strip()

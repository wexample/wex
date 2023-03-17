import datetime
import os
import click
from typing import List

from src.const.globals import LOG_MAX_DAYS


@click.command
@click.pass_obj
@click.option('--index', '-i', type=int, required=True)
@click.option('--search', '-s', type=str, required=True)
def core_autocomplete_suggest(kernel, index, search: str):
    suggestion = ''

    search_split = search.split(' ')
    search_part = search_split[index]

    if index == 1:
        suggestion = ' '.join(kernel.addons.keys())
    elif index == 2:
        suggestion = ':'
    elif index == 3:
        addon = search_split[1]

        if addon in kernel.registry['addons']:
            for command, command_data in kernel.registry['addons'][addon]['commands'].items():
                command_parts = command.split("::")
                command_split = command_parts[1].split("/")

                if "/" in search_part:
                    if command_split[0] == search_split[3].split('/')[0]:
                        suggestion += f' {" ".join(command_parts)}'
                else:
                    suggestion += f' {command_split[0]}'

        # Reduce unique values
        suggestion = " ".join(set(suggestion.split()))

    return suggestion


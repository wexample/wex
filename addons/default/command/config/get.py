import click
import os
import re

from src.const.globals import CONFIG_SEPARATOR_DEFAULT


@click.command
@click.option('--file', '-f', type=str, required=True)
@click.option('--key', '-k', type=str, required=True)
@click.option('--separator', '-s', required=True, default=CONFIG_SEPARATOR_DEFAULT)
@click.option('--default', '-d', default='')
def default_config_get(file, key, separator: str = CONFIG_SEPARATOR_DEFAULT, default='') -> str:
    if not file or not os.path.isfile(file):
        return ''

    with open(file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if re.search(r'^\s*' + re.escape(key) + r'\s*' + re.escape(separator), line):
            return re.split(separator, line)[-1].strip()

    return default

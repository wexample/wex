import os

import click

from src.helper.system import set_owner_recursively, get_user_or_sudo_user
from src.core.Kernel import Kernel
from src.decorator.command import command


@command()
@click.option('--path', '-p', type=str, required=False, default=None, help="Argument")
def system__own__this(kernel, path: str = None):
    if path is None:
        path = os.getcwd()

    kernel.log(f'Setting recursively ownership to "{get_user_or_sudo_user()}" on : {path}')
    set_owner_recursively(path)

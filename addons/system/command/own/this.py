import os

from src.helper.system import set_owner_recursively, get_user_or_sudo_user
from src.decorator.command import command
from src.decorator.option import option


@command(help="Make current user owner of this directory and every files or subdirectories")
@option('--path', '-p', type=str, required=False, default=None, help="Argument")
def system__own__this(kernel, path: str = None):
    if path is None:
        path = os.getcwd()

    kernel.io.log(f'Setting recursively ownership to "{get_user_or_sudo_user()}" on : {path}')
    set_owner_recursively(path)

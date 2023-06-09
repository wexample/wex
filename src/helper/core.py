import os

from src.const.globals import FILE_VERSION


def core_get_version(path: str) -> str:
    with open(f'{path}{FILE_VERSION}', 'r') as file:
        return file.read().strip()


def core_kernel_get_version(kernel) -> str:
    return core_get_version(kernel.path['root'])


def get_bashrc_handler_path(kernel):
    return os.path.join(kernel.path['root'], 'cli', "bashrc-handler")


def get_bashrc_handler_command(kernel):
    return f'. {get_bashrc_handler_path(kernel)}'

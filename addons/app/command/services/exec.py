import click

from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON


@click.command()
@click.pass_obj
@click.option('--hook', '-h', type=str, required=True,
              help="Hook name")
@click.option('--arguments', '-args', type=str, required=False,
              help="Hook name")
@click.option('--app-dir', '-a', type=str, required=True,
              help="App directory")
def app__services__exec(kernel, hook, arguments: str = '', app_dir: str = None):
    output = {}

    for service in kernel.addons['app']['config']['global']['services']:
        output[service] = kernel.exec(
            f'{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}{hook}',
            arguments,
            quiet=True
        )

    return output

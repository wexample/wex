import click

from addons.app.helpers.app import app_exec_in_workdir
from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON
from src.helper.args import parse_arg


@click.command()
@click.pass_obj
@click.option('--hook', '-h', type=str, required=True,
              help="Hook name")
@click.option('--arguments', '-args', type=str, required=False,
              help="Hook name")
@click.option('--app-dir', '-a', type=str, required=True,
              help="App directory")
def app__services__exec(kernel, app_dir: str, hook, arguments: str):
    def callback():
        nonlocal arguments
        output = {}

        arguments = parse_arg(arguments)

        for service in kernel.addons['app']['config']['global']['services']:
            output[service] = kernel.exec(
                f'{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}{hook}',
                arguments,
                quiet=True
            )

        return output

    return app_exec_in_workdir(
        kernel,
        app_dir,
        callback
    )

import click

from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON
from src.helper.args import parse_arg
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel


@click.command()
@click.pass_obj
@click.option('--hook', '-h', type=str, required=True,
              help="Hook name")
@click.option('--arguments', '-args', type=str, required=False,
              help="Arguments")
@app_dir_option()
def app__services__exec(kernel: Kernel, app_dir: str, hook, arguments: str):
    manager: AppAddonManager = kernel.addons['app']

    def callback():
        nonlocal arguments
        output = {}

        arguments = parse_arg(arguments)

        for service in manager.get_config('global.services'):
            arguments = arguments.copy()
            arguments['service'] = service

            output[service] = kernel.exec(
                f'{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}{hook}',
                arguments,
                quiet=True
            )

        return output

    return manager.exec_in_workdir(
        app_dir,
        callback
    )

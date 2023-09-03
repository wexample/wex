import click

from addons.app.command.services.exec import app__services__exec
from src.helper.args import parse_arg
from src.const.globals import COMMAND_CHAR_APP
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel


@click.command()
@click.pass_obj
@click.option('--hook', '-h', type=str, required=True,
              help="Hook name")
@click.option('--arguments', '-args', required=False,
              help="Hook name")
@app_dir_option()
def app__hook__exec(kernel: Kernel, hook, arguments, app_dir: str = None):
    arguments = parse_arg(arguments)

    if arguments is None:
        arguments = {}

    manager: AppAddonManager = kernel.addons['app']
    manager.log(f'Hooking : {hook}')

    arguments['app-dir'] = app_dir

    results = kernel.run_function(
        app__services__exec,
        {
            'app-dir': app_dir,
            'arguments': arguments,
            'hook': hook,
        }
    )

    results[COMMAND_CHAR_APP] = kernel.run_command(
        COMMAND_CHAR_APP + hook,
        arguments,
        quiet=True
    )

    return results

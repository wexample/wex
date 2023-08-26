import click

from addons.app.command.services.exec import app__services__exec
from src.helper.args import parse_arg
from src.const.globals import COMMAND_CHAR_APP


@click.command()
@click.pass_obj
@click.option('--hook', '-h', type=str, required=True,
              help="Hook name")
@click.option('--arguments', '-args', required=False,
              help="Hook name")
@click.option('--app-dir', '-a', type=str, required=True,
              help="App directory")
def app__hook__exec(kernel, hook, arguments, app_dir: str = None):
    arguments = parse_arg(arguments)

    results = kernel.exec_function(
        app__services__exec,
        {
            'app-dir': app_dir,
            'arguments': arguments,
            'hook': hook,
        }
    )

    results[COMMAND_CHAR_APP] = kernel.exec(
        COMMAND_CHAR_APP + hook,
        arguments,
        quiet=True
    )

    return results

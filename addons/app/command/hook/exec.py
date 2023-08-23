import click

from src.const.globals import COMMAND_CHAR_APP

from addons.app.command.services.exec import app__services__exec


@click.command()
@click.pass_obj
@click.option('--hook', '-h', type=str, required=True,
              help="Hook name")
@click.option('--arguments', '-args', type=str, required=False,
              help="Hook name")
@click.option('--app-dir', '-a', type=str, required=True,
              help="App directory")
def app__hook__exec(kernel, hook, arguments: str = '', app_dir: str = None):
    services_result = kernel.exec_function(
        app__services__exec,
        {
            'app-dir': app_dir,
            'arguments': arguments,
            'hook': hook,
        }
    )

    app_result = kernel.exec(
        COMMAND_CHAR_APP + hook,
        arguments,
        quiet=True
    )

    return services_result, app_result

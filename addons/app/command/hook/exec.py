
from addons.app.command.services.exec import app__services__exec
from src.helper.args import args_parse_one
from src.const.globals import COMMAND_CHAR_APP
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Exec a command on services and local app")
@option('--hook', '-h', type=str, required=True,
              help="Hook name")
@option('--arguments', '-args', required=False,
              help="Hook name")
def app__hook__exec(kernel: 'Kernel', hook, arguments, app_dir: str = None):
    arguments = args_parse_one(arguments)

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
    ).first()

    results[COMMAND_CHAR_APP] = kernel.run_command(
        COMMAND_CHAR_APP + hook,
        arguments,
        quiet=True
    )

    return results

from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON
from src.helper.args import args_parse_one
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Execute a command for all installed services")
@option('--hook', '-h', type=str, required=True,
        help="Hook name")
@option('--arguments', '-args', type=str, required=False,
        help="Arguments")
def app__services__exec(kernel: 'Kernel', app_dir: str, hook: str, arguments: str):
    manager: AppAddonManager = kernel.addons['app']

    output = {}

    arguments = args_parse_one(arguments, {})

    for service in manager.get_config('service', {}):
        arguments = arguments.copy()
        arguments['service'] = service

        command_name = f'{COMMAND_CHAR_SERVICE}{service}{COMMAND_SEPARATOR_ADDON}{hook}'

        manager.log(command_name)

        output[service] = kernel.run_command(
            command_name,
            arguments,
            quiet=True
        )

    return output

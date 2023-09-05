from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON
from src.helper.args import parse_arg
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option


@command(help="Execute a command for all installed services")
@option('--hook', '-h', type=str, required=True,
        help="Hook name")
@option('--arguments', '-args', type=str, required=False,
        help="Arguments")
@app_dir_option()
def app__services__exec(kernel: Kernel, app_dir: str, hook: str, arguments: str):
    manager: AppAddonManager = kernel.addons['app']

    output = {}

    arguments = parse_arg(arguments, {})

    for service in manager.get_config('global.services'):
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

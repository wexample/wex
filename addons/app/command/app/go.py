from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.command.app.exec import app__app__exec
from src.helper.dict import get_dict_item_by_path
from src.core import Kernel
from src.decorator.command import command
from src.decorator.option import option
from src.decorator.alias import alias


@command(help="Enter into app container")
@alias('app/go')
@app_dir_option()
@option('--container-name', '-cn', type=str, required=False, help="Container name if not configured")
@option('--user', '-u', type=str, required=False, help="User name or uid")
def app__app__go(kernel: Kernel, app_dir: str, container_name: str | None = None, user: str | None = None):

    shell_command = get_dict_item_by_path(
        kernel.registry,
        f'services.{container_name}.config.container.shell',
        '/bin/bash'
    )

    return kernel.run_function(
        app__app__exec,
        {
            'app-dir': app_dir,
            'container-name': container_name,
            # Ask to execute bash
            'command': shell_command,
            'user': user,
        }
    )

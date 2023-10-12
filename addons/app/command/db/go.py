from src.helper.dict import get_dict_item_by_path
from src.decorator.command import command
from src.core import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.command.app.exec import app__app__exec
from addons.app.command.services.exec import app__services__exec

@command(help="Enter into database management CLI")
@app_dir_option()
def app__db__go(
        kernel: Kernel,
        app_dir: str):
    container_name = 'mysql_8'

    shell_command = get_dict_item_by_path(
        kernel.registry,
        f'services.{container_name}.config.container.go',
        '/bin/bash'
    )

    # db_go_command = kernel.run_function(
    #     app__services__exec,
    #     {
    #         'app-dir': app_dir
    #     }
    # )


    # kernel.run_function(
    #     app__app__exec,
    #     {
    #         'app-dir': app_dir
    #     }
    # )

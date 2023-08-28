import click

from addons.app.command.hook.exec import app__hook__exec
from addons.app.helpers.app import app_log
from src.helper.system import set_owner_recursively, set_permissions_recursively, get_user_or_sudo_user
from addons.app.decorator.app_dir_option import app_dir_option


@click.command()
@click.pass_obj
@app_dir_option()
def app__app__perms(kernel, app_dir: str):
    user = get_user_or_sudo_user()

    app_log(kernel, f'Setting owner of all files to "{user}"')
    set_owner_recursively(app_dir)

    app_log(kernel, f'Setting file mode of all files to "755"')
    set_permissions_recursively(app_dir, 0o755)

    app_log(kernel, 'Updating app permissions...')
    kernel.exec_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'app/perms'
        }
    )

from addons.app.command.hook.exec import app__hook__exec
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.helper.system import set_owner_recursively, set_permissions_recursively, get_user_or_sudo_user
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel


@command(help="Set app files permissions")
@app_dir_option()
@as_sudo
def app__app__perms(kernel: Kernel, app_dir: str):
    manager: AppAddonManager = kernel.addons['app']
    user = get_user_or_sudo_user()

    manager.log(f'Setting owner of all files to "{user}"')
    set_owner_recursively(app_dir)

    manager.log(f'Setting file mode of all files to "755"')
    set_permissions_recursively(app_dir, 0o755)

    manager.log('Updating app permissions...')
    kernel.run_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'hook': 'app/perms'
        }
    )

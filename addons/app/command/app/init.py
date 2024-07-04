import os.path
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from git import Repo
from wexample_helpers.helpers.args_helper import args_split_arg_array
from wexample_helpers.helpers.string_helper import string_to_snake_case

from addons.app.command.app.start import app__app__start
from addons.app.command.hook.exec import app__hook__exec
from addons.app.command.service.install import app__service__install
from addons.app.const.app import APP_DIR_APP_DATA, ERR_SERVICE_NOT_FOUND
from addons.app.decorator.app_command import app_command
from addons.app.helper.app import app_create_env
from addons.core.command.service.resolve import core__service__resolve
from src.const.globals import COMMAND_TYPE_SERVICE
from src.const.types import CoreCommandCommaSeparatedList
from src.decorator.option import option
from src.helper.prompt import prompt_progress_steps

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Create new app and services configuration", dir_required=False)
@option("--name", "-n", type=str, required=False, help="Name of new app")
@option(
    "--git",
    "-g",
    is_flag=True,
    required=False,
    default=True,
    help="Initialize GIT repo",
)
@option("--app-dir", "-a", type=str, required=False, help="App directory")
@option(
    "--services", "-s", type=str, required=False, help="List of services to install"
)
@option(
    "--domains",
    "-d",
    type=str,
    required=False,
    help="Comma separated list of domains names",
)
@option("--env", "-e", type=str, required=False, help="App environment")
@option("--port", "-p", type=int, required=False, help="Port for web server")
@option(
    "--port-secure", "-ps", type=int, required=False, help="Secure port for web server"
)
def app__app__init(
    manager: "AppAddonManager",
    app_dir: str,
    name: Optional[str] = None,
    services: CoreCommandCommaSeparatedList = "",
    domains: str = "",
    git: bool = True,
    env: str | None = None,
    port: Optional[int] = None,
    port_secure: Optional[int] = None,
) -> None:
    kernel = manager.kernel
    current_dir = os.getcwd() + os.sep
    env = env or kernel.registry_structure.content.env

    # Resolve dependencies for all services
    services_resolved = list(
        kernel.run_function(
            core__service__resolve, {"service": args_split_arg_array(services)}
        ).first()
    )

    if not app_dir:
        app_dir = current_dir

    if not name:
        name = os.path.basename(os.path.dirname(app_dir))
    # Cleanup name.
    name_snake = string_to_snake_case(name)

    def _init_step_check_vars() -> None:
        kernel.io.log(f'Creating app in "{app_dir}"')

        kernel.io.log(f'Using name "{name_snake}"')

        if not os.path.exists(app_dir):
            os.makedirs(app_dir, exist_ok=True)

    def _init_step_check_services() -> Optional[bool]:
        if len(services_resolved) == 0:
            return None

        kernel.io.log("Checking services...")
        for service in services_resolved:
            if (
                not service
                in kernel.resolvers[COMMAND_TYPE_SERVICE].get_registry_data()
            ):
                kernel.io.error(ERR_SERVICE_NOT_FOUND, {"service": service})

                return False

        return None

    def _init_step_copy_app() -> None:
        import shutil

        app_sample_dir = (
            os.path.join(kernel.get_path("addons"), "app", "samples", "app") + "/"
        )

        os.makedirs(os.path.join(app_dir, APP_DIR_APP_DATA), exist_ok=True)

        shutil.copytree(
            app_sample_dir + APP_DIR_APP_DATA,
            os.path.join(app_dir, APP_DIR_APP_DATA),
            dirs_exist_ok=True,
            copy_function=shutil.copy2,
        )

        kernel.io.log("Renaming .sample files...")
        # Remove every .sample suffix after filenames
        # i.e .gitignore.sample becomes .gitignore
        app_data_path = os.path.join(app_dir, APP_DIR_APP_DATA)
        sample_files = list(Path(app_data_path).rglob("*.sample"))

        for sample_file in sample_files:
            new_file_name = os.path.splitext(sample_file)[0]
            os.rename(sample_file, new_file_name)
            kernel.io.log(f"Renaming {sample_file}")

    def _init_step_create_env() -> None:
        assert isinstance(app_dir, str)
        assert isinstance(env, str)

        kernel.io.log(f'Creating env file with env "{env}"')
        app_create_env(env, app_dir)

    def _init_step_create_config() -> None:
        nonlocal domains
        nonlocal manager

        kernel.io.log(f"Creating config...")

        domains_list = args_split_arg_array(domains)
        manager._config = manager.create_config(name_snake, domains_list)

        if port or port_secure:
            manager._config["port"] = {
                "public": port,
                "public_secure": port_secure,
            }

        manager.save_config()

    def _init_step_set_workdir() -> None:
        nonlocal manager

        manager.set_app_workdir(app_dir)

    def _init_step_install_service() -> None:
        for service in services_resolved:
            kernel.io.log(f"Installing service {service}")

            kernel.run_function(
                app__service__install,
                {
                    "app-dir": app_dir,
                    "service": service,
                    # Dependencies have already been resolved
                    "ignore-dependencies": True,
                },
            ).first()

    def _init_step_init_git() -> None:
        nonlocal git

        if git:
            kernel.io.log("Installing git repo...")

            Repo.init(app_dir)

    def _init_step_hooks() -> None:
        kernel.run_function(
            app__hook__exec, {"app-dir": app_dir, "hook": "app/init-post"}
        )

    def _init_step_unset_workdir() -> None:
        manager.unset_app_workdir(current_dir)

    def _init_step_complete() -> None:
        kernel.io.message_next_command(
            app__app__start, message=f"Your app has been created in {env} environment"
        )

    prompt_progress_steps(
        kernel,
        [
            _init_step_check_vars,
            _init_step_check_services,
            _init_step_copy_app,
            _init_step_create_env,
            _init_step_set_workdir,
            _init_step_create_config,
            _init_step_install_service,
            _init_step_init_git,
            _init_step_hooks,
            _init_step_unset_workdir,
            _init_step_complete,
        ],
    )

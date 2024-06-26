import os.path
import time
from typing import TYPE_CHECKING, Optional

import click

from addons.app.command.app.go import app__app__go
from addons.app.command.app.perms import app__app__perms
from addons.app.command.app.serve import app__app__serve
from addons.app.command.app.started import (
    APP_STARTED_CHECK_MODE_ANY_CONTAINER,
    app__app__started,
)
from addons.app.command.config.write import app__config__write
from addons.app.command.env.choose import app__env__choose
from addons.app.command.env.set import app__env__set
from addons.app.command.hook.exec import app__hook__exec
from addons.app.command.hosts.update import app__hosts__update
from addons.app.const.app import (
    APP_DIR_APP_DATA,
    APP_ENV_LOCAL,
    APP_FILEPATH_REL_COMPOSE_RUNTIME_YML,
    APP_FILEPATH_REL_ENV,
    HELPER_APP_PROXY_SHORT_NAME,
)
from addons.app.decorator.app_command import app_command
from addons.app.helper.docker import docker_exec_app_compose_command
from src.const.globals import CORE_COMMAND_NAME
from src.core.response.AbortResponse import AbortResponse
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.HiddenResponse import HiddenResponse
from src.core.response.InteractiveShellCommandResponse import (
    InteractiveShellCommandResponse,
)
from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager import (
    AbstractQueuedCollectionResponseQueueManager,
)
from src.core.response.queue_collection.QueuedCollectionStopResponse import (
    QueuedCollectionStopResponse,
)
from src.core.response.QueuedCollectionResponse import (
    QueuedCollectionResponse,
    QueuedCollectionResponseCollection,
)
from src.decorator.as_sudo import as_sudo
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@as_sudo()
@app_command(help="Start an app", should_be_valid=True)
@option(
    "--clear-cache",
    "-cc",
    is_flag=True,
    default=False,
    help="Forces a rebuild of images",
)
@option("--user", "-u", type=str, required=False, help="Owner of application files")
@option("--group", "-g", type=str, required=False, help="Group of application files")
@option("--env", "-e", type=str, required=False, help="App environment")
@option("--no-proxy", "-nopx", is_flag=True, required=False, help="Do not start proxy")
@option("--fast", "-f", is_flag=True, required=False, help="Do not rewrite config")
def app__app__start(
    manager: "AppAddonManager",
    app_dir: str,
    clear_cache: bool = False,
    user: Optional[str] = None,
    group: Optional[str] = None,
    env: Optional[str] = None,
    no_proxy: bool = False,
    fast: bool = False,
) -> QueuedCollectionResponse:
    kernel = manager.kernel
    name = manager.get_app_name()

    def _app__app__start__checkup(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> Optional[QueuedCollectionStopResponse]:
        nonlocal env

        if not os.path.exists(APP_FILEPATH_REL_ENV):
            if not env:
                if click.confirm(
                    "No .wex/.env file, would you like to create it ?", default=True
                ):
                    first = kernel.run_function(
                        app__env__choose,
                    ).first()

                    if isinstance(first, AbortResponse):
                        return QueuedCollectionStopResponse(
                            kernel, AbortResponse.reason
                        )

                    env = str(first)
            else:
                kernel.run_function(app__env__set, {"environment": env})

            kernel.io.message(f'Created .env file for environment "{env}"')

        if kernel.run_function(
            app__app__started,
            {"app-dir": app_dir, "mode": APP_STARTED_CHECK_MODE_ANY_CONTAINER},
        ).first():
            manager.log("App already running")
            return QueuedCollectionStopResponse(kernel, reason="APP_ALREADY_RUNNING")

        return None

    def _app__app__start__proxy(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> Optional[AbstractResponse]:
        nonlocal env

        # Current app is not the reverse proxy itself.
        if not manager.app_is_reverse_proxy(app_dir):
            # Env should have been defined at this point.
            env = manager.get_env(app_dir)

            if not manager.require_proxy():
                kernel.io.message(f"Don't require proxy")
                return None

            if no_proxy:
                kernel.io.message(f"Proxy explicitly disabled")
                return None

            proxy_path = manager.get_helper_app_path(HELPER_APP_PROXY_SHORT_NAME, env)

            # The reverse proxy is not running.
            if (
                not os.path.exists(proxy_path)
                or not kernel.run_function(
                    app__app__started,
                    {
                        "app-dir": proxy_path,
                        "mode": APP_STARTED_CHECK_MODE_ANY_CONTAINER,
                    },
                ).first()
            ):
                from addons.app.command.helper.start import app__helper__start

                return kernel.run_function(
                    app__helper__start,
                    {
                        "name": HELPER_APP_PROXY_SHORT_NAME,
                        "user": user,
                        "group": group,
                        "env": env,
                    },
                )

        return None

    def _app__app__start__config(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> AbstractResponse:
        kernel.run_function(app__app__perms, {"app-dir": app_dir})

        kernel.run_function(
            app__hook__exec, {"app-dir": app_dir, "hook": "app/start-pre"}
        )

        if manager.require_proxy():
            # Save app in proxy apps.
            manager.log("Registering app...")
            manager.add_proxy_app(name, app_dir)

        return kernel.run_function(
            app__config__write,
            {
                "app-dir": app_dir,
                "user": user,
                "group": group,
            },
        )

    def _app__app__start__start_hooks(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> HiddenResponse:
        # Load config after building
        manager.load_config()

        # Run docker compose
        compose_options = ["up", "-d"]

        if clear_cache:
            compose_options.append("--build")

        service_results = kernel.run_function(
            app__hook__exec,
            {
                "app-dir": app_dir,
                "hook": "app/start-options",
                "arguments": {"app-dir": app_dir, "options": compose_options},
            },
        ).first()

        compose_options += [
            item
            for value in service_results.values()
            if isinstance(value, list)
            for item in value
        ]

        return HiddenResponse(kernel, compose_options)

    def _app__app__start__starting(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> InteractiveShellCommandResponse:
        compose_files = queue.get_previous_value()
        assert isinstance(compose_files, list)

        return InteractiveShellCommandResponse(
            kernel,
            docker_exec_app_compose_command(
                kernel,
                app_dir,
                [APP_FILEPATH_REL_COMPOSE_RUNTIME_YML],
                compose_files,
            ),
        )

    def _app__app__start__update_hosts(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> None:
        manager.set_runtime_config("started", True)

        kernel.run_function(app__hosts__update)

    def _app__app__start__pending(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> None:
        def _check() -> bool:
            # Postpone execution
            response = kernel.run_function(
                app__hook__exec, {"app-dir": app_dir, "hook": "service/ready"}
            )

            responses = response.first()
            for context in responses:
                if (
                    context
                    and responses[context]
                    and responses[context].first() == False
                ):
                    kernel.io.log(f"@{context} is not running..")
                    return False

            return True

        while not _check():
            kernel.io.log(f"Waiting services..")
            time.sleep(2)

    def _app__app__start__serve(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> None:
        # Postpone execution
        kernel.run_function(
            app__hook__exec, {"app-dir": app_dir, "hook": "app/start-post"}
        )

        kernel.run_function(app__app__serve, {"app-dir": app_dir})

    def _app__app__start__first_init(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> None:
        env_dir = f"{manager.get_app_dir()}{APP_DIR_APP_DATA}"
        first_start_lock = os.path.join(
            env_dir, "tmp", f"{CORE_COMMAND_NAME}.first-start"
        )
        if not os.path.exists(first_start_lock):
            kernel.run_function(
                app__hook__exec, {"app-dir": app_dir, "hook": "app/first-init"}
            )

            with open(first_start_lock, "w") as file:
                file.write("1")

            manager.set_runtime_config("initialized", True)

    def _app__app__start__complete(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> str:
        env = manager.get_env()

        if manager.has_runtime_config("domains"):
            domains = manager.get_runtime_config("domains").get_list()
            domains_string = []

            for domain in domains:
                domains_string.append(
                    f'- http{"s" if env != APP_ENV_LOCAL else ""}://{domain}'
                )

            kernel.io.message(
                f'Your app is initialized as "{name}" in {env} environment',
                os.linesep.join(domains_string),
            )

        kernel.io.message_all_next_commands(
            [
                app__app__go,
            ]
        )

        return manager.get_app_dir()

    steps: QueuedCollectionResponseCollection

    if fast:
        steps = [
            # Just load docker compose
            _app__app__start__start_hooks,
            _app__app__start__starting,
        ]
    else:
        steps = [
            _app__app__start__checkup,
            _app__app__start__proxy,
            _app__app__start__config,
            _app__app__start__start_hooks,
            _app__app__start__starting,
            _app__app__start__update_hosts,
            _app__app__start__pending,
            _app__app__start__serve,
            _app__app__start__first_init,
            _app__app__start__complete,
        ]

    return QueuedCollectionResponse(
        kernel,
        steps,
    )

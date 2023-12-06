import time
from typing import TYPE_CHECKING

from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.helper.command import execute_command_sync

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Start the proxy", command_type=COMMAND_TYPE_SERVICE, should_run=True)
def proxy__app__start_post(
    manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    # TODO Pipeline inspect
    execute_command_sync(manager.kernel, ["docker", "ps"])
    execute_command_sync(manager.kernel, ["docker", "logs", "wex_proxy_local_proxy"])

    print("DEBUG WAIT 5")
    time.sleep(5)
    # Result : The file exists
    execute_command_sync(
        manager.kernel,
        ["cat", "/var/www/test/wex-proxy/.wex/tmp/docker-compose.runtime.yml"],
    )
    # Logs says that container is restarting (as I wait 5 seconds)
    execute_command_sync(manager.kernel, ["docker", "ps"])
    print("DEBUG INFO")
    # Docker config seems good
    execute_command_sync(manager.kernel, ["docker", "info"])
    print("DEBUG CURL")
    # Curl returns some data : {"Platform":{"Name":"Docker Engine - Community"},"... }
    execute_command_sync(
        manager.kernel, ["curl", "-v", "http://localhost:2375/version"]
    )
    print("DEBUG LOGS")
    # Logs returns an explicit message :
    # Info: running nginx-proxy version 1.3.1
    # ERROR: you need to share your Docker host socket with a volume at /tmp/docker.sock
    # Typically you should run your nginxproxy/nginx-proxy with: `-v /var/run/docker.sock:/tmp/docker.sock:ro`
    # See the documentation at: https://github.com/nginx-proxy/nginx-proxy/#usage
    execute_command_sync(manager.kernel, ["docker", "logs", "wex_proxy_local_proxy"])
    print("DEBUG INSPECT")
    # It returns a lot of info including :
    #         "State": {
    #             "Status": "restarting",
    #
    execute_command_sync(manager.kernel, ["docker", "inspect", "wex_proxy_local_proxy"])
    print("DEBUG LS")
    # The file does not exist !
    # total 0
    execute_command_sync(manager.kernel, ["ls", "-l", "/var/run/docker.sock"])
    print("DEBUG INSPECT 2")
    execute_command_sync(
        manager.kernel,
        ["docker", "inspect", "--format='{{.State.Status}}'", "wex_proxy_local_proxy"],
    )
    execute_command_sync(
        manager.kernel,
        [
            "docker",
            "run",
            "--rm",
            "-v",
            "/var/run/docker.sock:/var/run/docker.sock",
            "alpine",
            "ls",
            "-l",
            "/var/run/docker.sock",
        ],
    )

    time.sleep(5)
    execute_command_sync(
        manager.kernel,
        [
            "docker",
            "exec",
            "wex_proxy_local_proxy",
            "/bin/bash",
            "-c",
            "echo DEBUG_TEST",
        ],
    )
    execute_command_sync(
        manager.kernel,
        [
            "docker",
            "exec",
            "wex_proxy_local_proxy",
            "/bin/bash",
            "-c",
            "ln -fs /proc/1/fd/1 /var/log/nginx/access.log",
        ],
    )

    print("DEBUG")
    time.sleep(1)
    execute_command_sync(manager.kernel, ["docker", "ps"])
    execute_command_sync(
        manager.kernel,
        [
            "docker",
            "exec",
            "wex_proxy_local_proxy",
            "/bin/bash",
            "-c",
            "ln -fs /proc/1/fd/1 /var/log/nginx/access.log",
        ],
    )

    print("DEBUG")
    time.sleep(5)
    execute_command_sync(manager.kernel, ["docker", "ps"])
    execute_command_sync(
        manager.kernel,
        [
            "docker",
            "exec",
            "wex_proxy_local_proxy",
            "/bin/bash",
            "-c",
            "ln -fs /proc/1/fd/1 /var/log/nginx/access.log",
        ],
    )

    commands = [
        ["ln", "-fs", "/proc/1/fd/1", "/var/log/nginx/access.log"],
        ["ln", "-fs", "/proc/1/fd/1", "/var/log/nginx/error.log"],
        ["nginx", "-s", "reload"],
    ]

    for command in commands:
        manager.kernel.run_function(
            app__app__exec,
            {
                "app-dir": app_dir,
                # Ask to execute bash
                "command": command,
                "sync": True,
            },
        )

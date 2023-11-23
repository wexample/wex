from addons.app.helper.docker import docker_build_long_container_name
from src.helper.args import args_parse_one
from src.helper.command import command_to_string, command_escape
from src.decorator.option import option
from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.hook.exec import app__hook__exec
from src.core.response.NonInteractiveShellCommandResponse import NonInteractiveShellCommandResponse
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@app_command(help="Exec a command into app container", should_run=True)
@option('--container-name', '-cn', type=str, required=False, help="Container name if not configured")
@option('--command', '-c', type=str, required=True, help="Command to execute")
@option('--user', '-u', type=str, required=False, help="User name or uid")
@option('--sync', '-s', type=bool, is_flag=True, required=False, help="Execute command in a sub process")
@option('--interactive', '-tty', type=bool, is_flag=True, required=False, help="Interactive shell")
@option('--ignore-error', '-ie', type=bool, is_flag=True, required=False, help="Do not fail on error")
def app__app__exec(
        kernel: 'Kernel',
        app_dir: str,
        command: str,
        container_name: str | None = None,
        user: str | None = None,
        sync: bool = False,
        interactive: bool = False,
        ignore_error: bool = False) -> InteractiveShellCommandResponse | NonInteractiveShellCommandResponse:
    manager: AppAddonManager = kernel.addons['app']
    container_name = container_name or manager.get_main_container_name()

    docker_command = [
        'docker',
        'exec',
    ]

    if interactive:
        docker_command += [
            '-ti',
        ]

    if user:
        docker_command += [
            '-u',
            user
        ]

    # Allow to use /bin/bash or /bin/sh, or something else.
    shell_command = manager.get_service_shell()

    docker_command += [
        docker_build_long_container_name(kernel, container_name),
        shell_command
    ]

    enter_command = kernel.run_function(
        app__hook__exec,
        {
            'app-dir': app_dir,
            'arguments': {
                'container': container_name
            },
            'hook': 'app/exec',
        }
    )

    result = enter_command.first()
    sub_command = []
    for index in result:
        if result[index]:
            # Last result overrides previous to avoid
            # merging which can result to an unexpected final command
            sub_command = result[index].first()

    # Convert command in list to string
    command = args_parse_one(command)
    if isinstance(command, list):
        command = command_to_string(command)
    # In sync mode we pass command to Popen,
    # so we don't need to wrap it.
    elif not sync:
        command = command_escape(command)

    # Prepare the final command to be executed
    final_command = []

    if sub_command and len(sub_command):
        final_command += sub_command
        final_command += ['&&']

    # Add the main command
    final_command += [command]

    # Append the final command to docker_command
    docker_command += ['-c', command_to_string(final_command)]

    if sync:
        return NonInteractiveShellCommandResponse(
            kernel,
            docker_command,
            ignore_error
        )

    return InteractiveShellCommandResponse(
        kernel,
        docker_command,
        ignore_error
    )

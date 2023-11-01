from src.core.Kernel import Kernel
from addons.app.command.app.exec import app__app__exec
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE


@app_command(help="Start the proxy", command_type=COMMAND_TYPE_SERVICE, should_run=True)
def proxy__app__start_post(kernel: Kernel, app_dir: str, service: str):
    commands = [
        [
            'ln',
            '-fs',
            '/proc/1/fd/1',
            '/var/log/nginx/access.log'
        ],
        [
            'ln',
            '-fs',
            '/proc/1/fd/1',
            '/var/log/nginx/error.log'
        ],
        [
            'nginx',
            '-s',
            'reload',
        ]
    ]

    for command in commands:
        kernel.run_function(
            app__app__exec,
            {
                'app-dir': app_dir,
                # Ask to execute bash
                'command': command,
                'sync': True
            }
        )

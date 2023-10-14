from src.core.Kernel import Kernel
from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.decorator.service_option import service_option
from src.decorator.command import command
from addons.app.command.app.exec import app__app__exec


@command(help="Start the proxy")
@app_dir_option()
@service_option()
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

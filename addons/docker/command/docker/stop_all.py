from src.helper.process import process_post_exec
from src.core.Kernel import Kernel
from src.decorator.command import command


@command()
def docker__docker__stop_all(kernel: Kernel):
    # Containers
    process_post_exec(kernel, [
        'docker',
        'stop',
        [
            'docker',
            'ps',
            '-qa',
        ]
    ])

    # Networks
    process_post_exec(kernel, [
        'docker',
        'network',
        'rm',
        [
            'docker',
            'network',
            'ls',
            '-q',
            '--filter',
            'type=custom'
        ]
    ])

    # Volumes
    process_post_exec(kernel, [
        'docker',
        'volume',
        'rm',
        [
            'docker',
            'volume',
            'ls',
            '-q'
        ]
    ])

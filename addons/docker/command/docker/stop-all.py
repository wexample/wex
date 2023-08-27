import click

from src.helper.process import process_post_exec


@click.command()
@click.pass_obj
def docker__docker__stop_all(kernel):
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

from src.core.Kernel import Kernel
from src.decorator.command import command
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse


@command(help="Stop all running docker feature : containers, networks, volumes")
def docker__docker__stop_all(kernel: Kernel):
    return QueuedCollectionResponse(kernel, [
        InteractiveShellCommandResponse(kernel, [
            'docker',
            'stop',
            [
                'docker',
                'ps',
                '-qa',
            ]
        ], True),
        InteractiveShellCommandResponse(kernel, [
            'docker',
            'rm',
            [
                'docker',
                'ps',
                '-qa',
            ]
        ], True),
        InteractiveShellCommandResponse(kernel, [
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
        ], True),
        InteractiveShellCommandResponse(kernel, [
            'docker',
            'volume',
            'rm',
            [
                'docker',
                'volume',
                'ls',
                '-q'
            ]
        ], True),
    ])

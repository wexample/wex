from src.core.Kernel import Kernel
from src.decorator.command import command
from src.core.response.InteractiveShellCommandResponse import InteractiveShellCommandResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.alias_without_addon import alias_without_addon


@command(help="Stop all running docker feature : containers, networks, volumes")
@alias_without_addon()
def docker__docker__stop_all(kernel: Kernel):
    return ResponseCollectionResponse(kernel, [
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

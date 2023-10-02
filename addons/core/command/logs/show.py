from src.decorator.alias import alias
from src.decorator.command import command
from src.core import Kernel
import os
import json


@command(help="Description")
@alias('logs')
def core__logs__show(kernel: Kernel, max: int = 10) -> str:
    output = []
    directory = kernel.path['log']

    all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    json_files = [f for f in all_files if f.endswith('.json')]
    sorted_files = sorted(json_files)
    last_files = sorted_files[-max:]

    for filename in last_files:
        with open(os.path.join(directory, filename), 'r') as file:
            data = json.load(file)

            for command_data in data['commands']:
                output.append(' | '.join([
                    data['dateStart'],
                    command_data['command']
                ]))

    return "\n".join(output)

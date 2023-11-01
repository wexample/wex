from src.decorator.alias import alias
from src.decorator.command import command
from src.core import Kernel
import json


@command(help="Description")
@alias('logs')
def core__logs__show(kernel: Kernel, max: int = 10) -> str:
    output = []
    files = kernel.logger.get_all_logs_files()
    last_files = files[-max:]

    for filepath in last_files:
        with open(filepath) as file:
            data = json.load(file)

            for command_data in data['commands']:
                output.append(' | '.join([
                    data['dateStart'],
                    command_data['command']
                ]))

    return "\n".join(output)

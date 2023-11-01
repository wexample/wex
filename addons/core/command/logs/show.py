from src.decorator.alias import alias
from src.decorator.no_log import no_log
from src.decorator.command import command
from src.core import Kernel
import json
from src.core.response.DataSet2dResponse import DataSet2dResponse


@command(help="Show a summary of log files")
@alias('logs')
@no_log
def core__logs__show(kernel: Kernel, max: int = 10) -> str:
    output = []
    files = kernel.logger.get_all_logs_files()
    last_files = files[-max:]
    response = DataSet2dResponse(kernel)

    response.set_header([
        'Command',
        'Date',
        'Status'
    ])

    for filepath in last_files:
        with open(filepath) as file:
            data = json.load(file)

            output.append([
                data['dateStart'],
                data['commands'][0]['command'] if len(data['commands']) else '-',
                data['status']
            ])

    response.set_body(output)

    return response

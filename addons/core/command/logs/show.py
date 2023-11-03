from src.helper.json import load_json_if_valid
from src.decorator.alias import alias
from src.decorator.no_log import no_log
from src.decorator.command import command
from src.core import Kernel
from src.core.response.TableResponse import TableResponse


@command(help="Show a summary of log files")
@alias('logs')
@no_log()
def core__logs__show(kernel: Kernel, max: int = 10) -> str:
    output = []
    files = kernel.logger.get_all_logs_files()
    last_files = files[-max:]
    response = TableResponse(kernel)

    response.set_header([
        'Command',
        'Date',
        'Status'
    ])

    for filepath in last_files:
        log = load_json_if_valid(filepath)

        if log:
            output.append(
                kernel.logger.build_summary(
                    log
                )
            )

    response.set_body(output)

    return response

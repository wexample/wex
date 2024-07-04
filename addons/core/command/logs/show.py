from typing import TYPE_CHECKING, cast

from wexample_helpers.helpers.json_helper import json_load_if_valid

from src.core.Logger import LoggerLogData
from src.core.response.TableResponse import TableBody, TableBodyLine, TableResponse
from src.decorator.alias import alias
from src.decorator.command import command
from src.decorator.no_log import no_log

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


@alias("logs")
@no_log()
@command(help="Show a summary of log files")
def core__logs__show(kernel: "Kernel", max: int = 10) -> TableResponse:
    output: TableBody = []
    files = kernel.logger.get_all_logs_files()
    last_files = files[-max:]
    response = TableResponse(kernel)

    response.set_header(["Command", "Date", "Status"])

    for filepath in last_files:
        log = json_load_if_valid(filepath)

        if log:
            output.append(
                cast(
                    TableBodyLine, kernel.logger.build_summary(cast(LoggerLogData, log))
                )
            )

    response.set_body(output)

    return response

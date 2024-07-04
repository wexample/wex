from typing import TYPE_CHECKING

import psutil

from addons.ai.decorator.ai_tool import ai_tool
from src.core.response.TableResponse import TableBody, TableResponse
from src.decorator.command import command
from src.helper.file import file_get_human_readable_size

if TYPE_CHECKING:
    from src.utils.kernel import Kernel


@ai_tool()
@command(help="Return space usage of current system disks")
def system__disk__spaces(kernel: "Kernel") -> TableResponse:
    output_list = TableResponse(kernel)
    output_list.set_header(
        [
            "Size",
            "Used",
            "Avail",
            "Usage",
            "Mounted",
            "Filesystem",
        ]
    )

    body: TableBody = []
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)

        body.append(
            [
                file_get_human_readable_size(usage.total),
                file_get_human_readable_size(usage.used),
                file_get_human_readable_size(usage.free),
                usage.percent,
                partition.mountpoint,
                partition.device,
            ]
        )

    output_list.set_body(body)

    return output_list

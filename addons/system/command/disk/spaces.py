import psutil

from src.core.response.DataSet2dResponse import DataSet2dResponse
from src.helper.file import human_readable_size
from src.core.Kernel import Kernel
from src.decorator.command import command


@command(help="Return space usage of current system disks")
def system__disk__spaces(kernel: Kernel):
    output_list = DataSet2dResponse(kernel)
    output_list.set_header([
        'Size',
        'Used',
        'Avail',
        'Usage',
        'Mounted',
        'Filesystem',
    ])

    body = []
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)

        body.append([
            human_readable_size(usage.total),
            human_readable_size(usage.used),
            human_readable_size(usage.free),
            usage.percent,
            partition.mountpoint,
            partition.device,
        ])

    output_list.set_body(body)

    return output_list.render()

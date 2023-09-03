import click
import psutil

from src.core.response.DataSet2dResponse import DataSet2dResponse
from src.helper.file import human_readable_size


@click.command()
@click.pass_obj
def system__disk__spaces(kernel):
    output_list = DataSet2dResponse()
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

    return output_list.render(kernel)



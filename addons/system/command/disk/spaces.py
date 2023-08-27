import click
import psutil

from src.helper.file import human_readable_size


@click.command()
def system__disk__spaces():
    print("Filesystem      Size  Used  Avail Use% Mounted on")
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        print(
            f"{partition.device:<15} "
            f"{human_readable_size(usage.total):<7} "
            f"{human_readable_size(usage.used):<7} "
            f"{human_readable_size(usage.free):<7} "
            f"{usage.percent}%    "
            f"{partition.mountpoint}"
        )

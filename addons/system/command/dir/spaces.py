import click
import os

from src.helper.file import human_readable_size


@click.command()
@click.option('--dir', '-d', type=str, required=False, help="Directory to inspect")
def system__dir__spaces(dir: str = None):
    if dir is None:
        dir = os.getcwd()

    def get_dir_size(directory):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    dir_list = [os.path.join(dir, d) for d in os.listdir(dir) if
                os.path.isdir(os.path.join(dir, d))]
    file_list = [os.path.join(dir, f) for f in os.listdir(dir) if
                 os.path.isfile(os.path.join(dir, f))]
    all_list = dir_list + file_list

    sizes = {}
    for entry in all_list:
        if os.path.isdir(entry):
            sizes[entry] = get_dir_size(entry)
        else:
            sizes[entry] = os.path.getsize(entry)

    # Sort by size
    sorted_sizes = {k: v for k, v in sorted(sizes.items(), key=lambda item: item[1])}

    # Print sorted list in human-readable format
    for k, v in sorted_sizes.items():
        print(f"{human_readable_size(v)}\t\t{os.path.basename(k)}")



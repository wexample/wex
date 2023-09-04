import os

from src.helper.file import human_readable_size
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option
from src.core.response.DataSet2dResponse import DataSet2dResponse


@command()
@option('--dir', '-d', type=str, required=False, help="Directory to inspect")
def system__dir__spaces(kernel: Kernel, dir: str = None):
    if dir is None:
        dir = os.getcwd()

    def get_dir_size(directory):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    # Initialize DataSet2dResponse object
    output_list = DataSet2dResponse(kernel)
    output_list.set_header(['Size', 'Name'])

    dir_list = [os.path.join(dir, d) for d in os.listdir(dir) if
                os.path.isdir(os.path.join(dir, d))]
    file_list = [os.path.join(dir, f) for f in os.listdir(dir) if
                 os.path.isfile(os.path.join(dir, f))]
    all_list = dir_list + file_list

    body = []
    for entry in all_list:
        if os.path.isdir(entry):
            size = get_dir_size(entry)
        else:
            size = os.path.getsize(entry)

        body.append([human_readable_size(size), os.path.basename(entry)])

    output_list.set_body(body)

    return output_list.render(kernel)

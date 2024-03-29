import os
from typing import TYPE_CHECKING, Optional, cast

from addons.ai.decorator.ai_tool import ai_tool
from src.core.response.TableResponse import TableBody, TableResponse
from src.decorator.command import command
from src.decorator.option import option
from src.helper.file import file_get_human_readable_size

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@ai_tool()
@command(help="Return sizes of current directory subdirectories")
@option("--dir", "-d", type=str, required=False, help="Directory to inspect")
def system__dir__spaces(kernel: "Kernel", dir: Optional[str] = None) -> TableResponse:
    dir = dir or os.getcwd()

    # Function to calculate directory size
    def get_dir_size(directory: str) -> int:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    try:
                        total_size += os.path.getsize(fp)
                    except OSError:
                        pass
        return total_size

    # Initialize TableResponse object
    output_list = TableResponse(kernel)
    output_list.set_header(["Size", "Name"])

    dir_list = [
        os.path.join(dir, d)
        for d in os.listdir(dir)
        if os.path.isdir(os.path.join(dir, d))
    ]
    file_list = [
        os.path.join(dir, f)
        for f in os.listdir(dir)
        if os.path.isfile(os.path.join(dir, f))
    ]
    all_list = dir_list + file_list

    body: TableBody = []
    for entry in all_list:
        size = None
        if os.path.isdir(entry):
            size = get_dir_size(entry)
        elif os.path.isfile(entry):
            size = os.path.getsize(entry)

        if size is not None:
            # Storing raw size as a third element in the list for sorting later
            body.append(
                [file_get_human_readable_size(size), os.path.basename(entry), size]
            )

    # Sort the list by raw size (the third element of each sublist)
    # The sort will be in ascending order, meaning smallest files will come first and largest last.
    body_sorted = cast(TableBody, sorted(body, key=lambda x: x[2]))

    # Remove the raw size from the list
    body_sorted = [[human_readable, name] for human_readable, name, _ in body_sorted]

    output_list.set_body(body_sorted)

    return output_list

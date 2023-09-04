import os

from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option


@command()
@option('--file-path', '-f', type=str, required=True,
        help="File to work on")
@option('--line', '-l', type=str, required=True,
        help="Exact line, ending an trailing spaces will be ignored")
def default__file__remove_line(kernel: Kernel, file_path: str, line: str) -> None:
    if not os.path.isfile(file_path):
        kernel.log("File does not exist.")
        return

    # Ensure line has no leading/trailing white space
    line = line.strip()

    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for existing_line in lines:
            # Ignore empty lines and the line to remove
            if existing_line.strip() != "" and existing_line.strip() != line:
                file.write(existing_line)

import os
import click


@click.command
@click.pass_obj
@click.option('--file-path', '-f', type=str, required=True)
@click.option('--line', '-l', type=str, required=True)
def default__file__remove_line(kernel, file_path: str, line: str) -> None:
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
                file.write(line)

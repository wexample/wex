import click


@click.command
@click.option('--file', '-f', type=str, required=True)
@click.option('--line', '-l', type=str, required=True)
def default_file_append_once(file: str, line: str) -> None:
    """
    Append a line to a file if it doesn't exist already.

    :param file: path to the file
    :param line: line to append to the file
    :return: None
    """
    # Open the file in read mode
    with open(file, 'r') as f:
        # Check if the line exists already
        if line in f.read():
            return

    # Open the file in append mode and write the line
    with open(file, 'a') as f:
        f.write(line + '\n')

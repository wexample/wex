import click

from src.core.Kernel import Kernel
from src.decorator.command import command


@command()
@click.option('--file', '-f', type=str, required=True,
              help="File to work on")
@click.option('--line', '-l', type=str, required=True,
              help="Line to add if not already there somewhere in the file")
def default__file__append_once(kernel: Kernel, file: str, line: str) -> None:
    """
    Append a line to a file if it doesn't exist already.
    """
    # Initialise a variable to store the last character of the file
    last_char = None

    # Open the file in read mode
    with open(file, 'r') as f:
        # Check if the line exists already
        content = f.read()
        if line in content:
            return
        # Store the last character of the file if it is not empty
        if content:
            last_char = content[-1]

    # Open the file in append mode and write the line
    with open(file, 'a') as f:
        # If the last character is not a newline, add one
        if last_char != '\n':
            f.write('\n')
        f.write(line + '\n')

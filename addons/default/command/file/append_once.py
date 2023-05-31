import click


@click.command
@click.option('--file', '-f', type=str, required=True)
@click.option('--line', '-l', type=str, required=True)
def default__file__append_once(file: str, line: str) -> None:
    """
    Append a line to a file if it doesn't exist already.

    :param file: path to the file
    :param line: line to append to the file
    :return: None
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

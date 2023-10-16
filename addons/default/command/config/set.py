import click

from src.const.globals import CONFIG_SEPARATOR_DEFAULT


@click.command
@click.pass_obj
@click.option('--file', '-f', type=str, required=True)
@click.option('--key', '-k', type=str, required=True)
@click.option('--value', '-v', required=True)
@click.option('--separator', '-s', required=True, default=CONFIG_SEPARATOR_DEFAULT)
@click.option('--verbose', '-vv', type=bool, default=False, is_flag=True)
def default__config__set(kernel, file, key, value, separator: str = CONFIG_SEPARATOR_DEFAULT, verbose: bool=False):
    if verbose:
        kernel.log(f'Setting variable {key}{separator}{value} in {file}')

    with open(file, 'r') as f:
        lines = f.readlines()

    updated_lines = []
    found_key = False

    for line in lines:
        if line.startswith(f"{key}{separator}"):
            updated_lines.append(f"{key}{separator}{value}\n")
            found_key = True
        else:
            updated_lines.append(line)

    if not found_key:
        # Add a new line if the file doesn't end with a newline
        if lines and not lines[-1].endswith('\n'):
            updated_lines.append('\n')
        # Add a new line if the file doesn't contain any content
        if not lines:
            updated_lines.append('\n')
        updated_lines.append(f"{key}{separator}{value}\n")

    with open(file, 'w') as f:
        f.writelines(updated_lines)

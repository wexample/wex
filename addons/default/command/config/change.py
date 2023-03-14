import click

CONFIG_SEPARATOR_DEFAULT = ' = '


@click.command()
@click.option('--file', '-f', type=str, required=True)
@click.option('--key', '-k', type=str, required=True)
@click.option('--value', '-v', required=True)
@click.option('--separator', '-s', required=True, default=CONFIG_SEPARATOR_DEFAULT)
def default_config_change(file, key, value, separator: str = CONFIG_SEPARATOR_DEFAULT):
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
        updated_lines.append(f"{key}{separator}{value}\n")

    with open(file, 'w') as f:
        f.writelines(updated_lines)

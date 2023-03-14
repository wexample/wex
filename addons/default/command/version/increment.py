import click


@click.command()
@click.option('--version', '-v', type=str, required=True)
@click.option('--type', '-t', type=str, default='minor', help="Upgrade type (major, intermediate or minor)")
@click.option('--increment', '-i', type=int, default=1, help="Amount of version to increment")
def default_version_increment(version, type, increment) -> str:
    major, intermediate, minor = version.split('.')

    # Increment according type.
    if type == 'major':
        major = str(int(major) + increment)
        intermediate, minor = '0', '0'
    elif type == 'intermediate':
        intermediate = str(int(intermediate) + increment)
        minor = '0'
    else:  # type == 'minor'
        minor = str(int(minor) + increment)

    # Set to zero in result is negative.
    if int(major) < 0:
        major, intermediate, minor = '0', '0', '0'
    elif int(intermediate) < 0:
        intermediate, minor = '0', '0'
    elif int(minor) < 0:
        minor = '0'

    return f"{major}.{intermediate}.{minor}"

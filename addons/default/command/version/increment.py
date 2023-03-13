import click


@click.command()
@click.option('--version', '-v', type=str, required=True)
@click.option('--type', '-t', type=str, default='minor', help="Upgrade type (major, intermediate or minor)")
@click.option('--increment', '-i', type=int, default=1, help="Amount of version to increment")
def default_version_increment(version, type, increment) -> str:
    major, minor, build = version.split('.')

    # Increment according type.
    if type == 'major':
        major = str(int(major) + increment)
        minor, build = '0', '0'
    elif type == 'intermediate':
        minor = str(int(minor) + increment)
        build = '0'
    else:  # type == 'minor'
        build = str(int(build) + increment)

    # Set to zero in result is negative.
    if int(major) < 0:
        major, minor, build = '0', '0', '0'
    elif int(minor) < 0:
        minor, build = '0', '0'
    elif int(build) < 0:
        build = '0'

    return f"{major}.{minor}.{build}"

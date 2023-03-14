import click
import datetime


@click.command()
@click.option('--version', '-v', type=str, required=True)
@click.option('--type', '-t', type=str, default='minor', help="Upgrade type (major, intermediate or minor)")
@click.option('--increment', '-i', type=int, default=1, help="Amount of version to increment")
def default_version_increment(version: str, type: str, increment: str) -> str:
    pre_build_number = 1

    # Handle 1.0.0-beta.1+build.1234
    if '-' in version:
        base_version, pre_build = version.split('-')

        if '.' in pre_build:
            pre_build_parts = pre_build.split('.')
            if len(pre_build_parts) == 2:
                pre_build, pre_build_number = pre_build_parts
            else:
                pre_build, pre_build_number, _ = pre_build_parts

            # pre_build_number can be : 1+build.1234
            if '+' in pre_build_number:
                # Ignore last part which is a timestamp.
                pre_build_number: int = int(pre_build_number.split('+')[0])
            else:
                pre_build_number: int = int(pre_build_number)
    else:
        base_version, pre_build = version, ''

    major, intermediate, minor = base_version.split('.')
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Increment according type.
    if type == 'major':
        major = str(int(major) + increment)
        intermediate, minor = '0', '0'
    elif type == 'intermediate':
        intermediate = str(int(intermediate) + increment)
        minor = '0'
    # Any of pre-build version.
    elif type == 'alpha' or type == 'beta' or type == 'dev' or type == 'rc' or type == 'nightly' or type == 'snapshot':
        pre_build = type
        pre_build_number += increment
    else:  # type == 'minor'
        minor = str(int(minor) + increment)

    # Set to zero in result is negative.
    if int(major) < 0:
        major, intermediate, minor = '0', '0', '0'
    elif int(intermediate) < 0:
        intermediate, minor = '0', '0'
    elif int(minor) < 0:
        minor = '0'

    build_info = ''
    if pre_build:
        build_info = f'-{pre_build}.{pre_build_number}'

    print(f"{major}.{intermediate}.{minor}{build_info}+build.{timestamp}")

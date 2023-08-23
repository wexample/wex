import click
import datetime

# Upgrade types
UPGRADE_TYPE_MAJOR = 'major'
UPGRADE_TYPE_INTERMEDIATE = 'intermediate'
UPGRADE_TYPE_MINOR = 'minor'
UPGRADE_TYPE_ALPHA = 'alpha'
UPGRADE_TYPE_BETA = 'beta'
UPGRADE_TYPE_DEV = 'dev'
UPGRADE_TYPE_RC = 'rc'
UPGRADE_TYPE_NIGHTLY = 'nightly'
UPGRADE_TYPE_SNAPSHOT = 'snapshot'

VERSION_PRE_BUILD_NUMBER = 0
VERSION_BUILD_TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M%S")


@click.command
@click.option('--version', '-v', type=str, required=True,
              help="Base version to increment")
def default__version__increment(
        version: str,
        upgrade_type: str = UPGRADE_TYPE_MINOR,
        increment: int = 1,
        build: bool = False
) -> str:
    pre_build_number: int = VERSION_PRE_BUILD_NUMBER

    # Handle 1.0.0-beta.1+build.1234
    if '-' in version:
        base_version, pre_build = version.split('-')

        if '.' in pre_build:
            pre_build_parts = pre_build.split('.')
            if len(pre_build_parts) == 2:
                pre_build, pre_build_number = pre_build_parts
            else:
                pre_build, pre_build_number, _ = pre_build_parts

            upgrade_type = pre_build

            # pre_build_number can be : 1+build.1234
            if '+' in pre_build_number:
                # Ignore last part which is a timestamp.
                pre_build_number = int(pre_build_number.split('+')[0])
            else:
                pre_build_number = int(pre_build_number)
    else:
        base_version, pre_build = version, ''

    major, intermediate, minor = base_version.split('.')

    # Increment according type
    if upgrade_type == UPGRADE_TYPE_MAJOR:
        major = str(int(major) + increment)
        intermediate, minor = '0', '0'
    elif upgrade_type == UPGRADE_TYPE_INTERMEDIATE:
        intermediate = str(int(intermediate) + increment)
        minor = '0'
    # Any of pre-build version
    elif upgrade_type in [
        UPGRADE_TYPE_ALPHA,
        UPGRADE_TYPE_BETA,
        UPGRADE_TYPE_DEV,
        UPGRADE_TYPE_RC,
        UPGRADE_TYPE_NIGHTLY,
        UPGRADE_TYPE_SNAPSHOT
    ]:
        pre_build_number += increment
    # type == 'minor' or everything else
    else:
        minor = str(int(minor) + increment)

    # Set to zero in result is negative
    if int(major) < 0:
        major, intermediate, minor = '1', '0', '0'
    elif int(intermediate) < 0:
        intermediate, minor = '0', '0'
    elif int(minor) < 0:
        minor = '0'

    # Build version string
    pre_build_info = ''
    if pre_build:
        pre_build_info = f'-{pre_build}.{pre_build_number}'

    return f"{major}.{intermediate}.{minor}{pre_build_info}{'+build.' + VERSION_BUILD_TIMESTAMP if build else ''}"

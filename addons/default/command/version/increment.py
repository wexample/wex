from addons.default.command.version.parse import default__version__parse
from src.decorator.command import command
from src.core import Kernel

from addons.default.const.default import UPGRADE_TYPE_MINOR, VERSION_PRE_BUILD_NUMBER, UPGRADE_TYPE_MAJOR, \
    UPGRADE_TYPE_INTERMEDIATE, UPGRADE_TYPE_ALPHA, UPGRADE_TYPE_BETA, UPGRADE_TYPE_DEV, UPGRADE_TYPE_RC, \
    UPGRADE_TYPE_NIGHTLY, UPGRADE_TYPE_SNAPSHOT, VERSION_BUILD_TIMESTAMP
from src.decorator.option import option


@command(help="Increment giver version number string")
@option('--version', '-v', type=str, required=True,
        help="Base version to increment")
def default__version__increment(
        kernel: Kernel,
        version: str,
        upgrade_type: str = UPGRADE_TYPE_MINOR,
        increment: int = 1,
        build: bool = False
) -> str:
    version_dict = kernel.run_function(
        default__version__parse,
        {'version': version}
    )

    major = version_dict['major']
    intermediate = version_dict['intermediate']
    minor = version_dict['minor']
    pre_build_type = version_dict['pre_build_type']
    pre_build_number = version_dict['pre_build_number'] or VERSION_PRE_BUILD_NUMBER

    # Increment according to type
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
    if pre_build_type:
        pre_build_info = f'-{pre_build_type}.{pre_build_number}'

    return f"{major}.{intermediate}.{minor}{pre_build_info}{'+build.' + VERSION_BUILD_TIMESTAMP if build else ''}"

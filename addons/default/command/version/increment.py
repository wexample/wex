from addons.default.command.version.parse import default__version__parse
from addons.default.helpers.version import version_join
from src.decorator.command import command
from src.core import Kernel

from addons.default.const.default import UPGRADE_TYPE_MINOR, UPGRADE_TYPE_MAJOR, \
    UPGRADE_TYPE_INTERMEDIATE, UPGRADE_TYPE_ALPHA, UPGRADE_TYPE_BETA, UPGRADE_TYPE_DEV, UPGRADE_TYPE_RC, \
    UPGRADE_TYPE_NIGHTLY, UPGRADE_TYPE_SNAPSHOT
from src.decorator.option import option


@command(help="Increment giver version number string")
@option('--version', '-v', type=str, required=True,
        help="Base version to increment")
@option('--type', '-t', type=str, required=False,
        help="Type of update")
@option('--increment', '-i', required=False, type=int, default=1,
        help="Type of update")
@option('--build', '-b', is_flag=True, required=False, default=False,
        help="Include build number")
def default__version__increment(
        kernel: Kernel,
        version: str,
        type: str = UPGRADE_TYPE_MINOR,
        increment: int = 1,
        build: bool = False
) -> str:
    version_dict = kernel.run_function(
        default__version__parse,
        {'version': version}
    ).first()

    # Increment according to type
    if type == UPGRADE_TYPE_MAJOR:
        version_dict['major'] = str(int(version_dict['major']) + increment)
        version_dict['intermediate'], version_dict['minor'] = '0', '0'
    elif type == UPGRADE_TYPE_INTERMEDIATE:
        version_dict['intermediate'] = str(int(version_dict['intermediate']) + increment)
        version_dict['minor'] = '0'
    # Any of pre-build version
    elif type in [
        UPGRADE_TYPE_ALPHA,
        UPGRADE_TYPE_BETA,
        UPGRADE_TYPE_DEV,
        UPGRADE_TYPE_RC,
        UPGRADE_TYPE_NIGHTLY,
        UPGRADE_TYPE_SNAPSHOT
    ]:
        version_dict['pre_build_number'] += increment
    # type == 'version_dict['minor']' or everything else
    else:
        version_dict['minor'] = str(int(version_dict['minor']) + increment)

    # Set to zero if result is negative
    if int(version_dict['major']) < 0:
        version_dict['major'], version_dict['intermediate'], version_dict['minor'] = '1', '0', '0'
    elif int(version_dict['intermediate']) < 0:
        version_dict['intermediate'], version_dict['minor'] = '0', '0'
    elif int(version_dict['minor']) < 0:
        version_dict['minor'] = '0'

    return version_join(version_dict, build)

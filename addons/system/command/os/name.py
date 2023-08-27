import platform
import click

OS_NAME_LINUX = 'linux'
OS_NAME_MAC = 'mac'
OS_NAME_UNDEFINED = 'undefined'
OS_NAME_WINDOWS = 'windows'


@click.command(help="Return the local OS name.")
def system__os__name():
    os_name = platform.system()

    if os_name == "Darwin":
        return OS_NAME_MAC
    elif os_name == "Linux":
        return OS_NAME_LINUX
    elif os_name in ["CYGWIN", "MINGW32", "MINGW64", "MSYS"]:
        return OS_NAME_WINDOWS
    else:
        return OS_NAME_UNDEFINED

import platform
import click


@click.command(help="Return the local OS name.")
def system__os__name():
    os_name = platform.system()

    if os_name == "Darwin":
        return "mac"
    elif os_name == "Linux":
        return "linux"
    elif os_name in ["CYGWIN", "MINGW32", "MINGW64", "MSYS"]:
        return "windows"
    else:
        return "undefined"

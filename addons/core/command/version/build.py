import click
from addons.default.command.version.increment import default__version__increment
from src.helper.core import core_get_version


@click.command
@click.pass_obj
def core__version__build(kernel) -> None:
    version = core_get_version(kernel.path["root"])

    kernel.log(f'Building from {version}...')

    new_version = default__version__increment.callback(
        version,
    )

    kernel.log(f'New version : {new_version}', increment=1)

    # Write new_version to file
    with open(f'{kernel.path["root"]}version.txt', 'w') as version_file:
        version_file.write(str(new_version))

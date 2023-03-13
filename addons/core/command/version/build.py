import click


@click.command()
@click.pass_obj
def core_version_build(kernel) -> None:
    print('Building new version...')
    print(kernel.version)

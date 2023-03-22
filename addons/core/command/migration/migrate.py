import click

@click.command()
@click.pass_obj
@click.option('--arg', '-a', type=str, required=True, help="Argument")
def core_migration_migrate(kernel, arg):
    pass

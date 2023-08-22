import click


@click.command()
@click.option('--option', '-o', is_flag=True, required=False)
@click.option('--another-option', '-ao', is_flag=True, required=False)
def service__test__first():
    return 'FIRST'

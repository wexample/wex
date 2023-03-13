import click
@click.command()
@click.option('--myarg', type=str)
@click.option('-d', is_flag=True, type=bool)
@click.option('-f', is_flag=True, type=bool)
def core_registry_build(myarg, d, f):
    print('Building registry...')

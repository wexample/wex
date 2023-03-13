import click


@click.command()
@click.pass_obj
@click.pass_context
@click.option('--myarg', type=str)
@click.option('-d', is_flag=True, type=bool)
@click.option('-f', is_flag=True, type=bool)
def core_registry_build(ctx, kernel, myarg, d, f):
    print('Building registry...')
    print(kernel.version)

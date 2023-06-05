import click


@click.command()
@click.pass_obj
@click.option('--arg', '-a', type=str, required=True, help="Argument")
def {function_name}(kernel, arg):
    pass

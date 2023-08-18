import click


@click.command
@click.option('--arg_one', '-a', type=str, required=True)
def app__local_command__test(arg_one: str):
    return f'OK:{arg_one}'

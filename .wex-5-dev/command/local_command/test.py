import click


@click.command
@click.option('--local-option', '-lo', required=False)
def app__local_command__test(local_option: str):
    return f'OK:{local_option}'

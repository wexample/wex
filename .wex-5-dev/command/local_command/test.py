import click

@click.command()
@click.option('--local_option', '-lo', is_flag=True, required=False)
def app__local_command__test():
    print('OK')

import os
import click


@click.command()
def system__system__is_docker():
    return os.path.exists('/.dockerenv')

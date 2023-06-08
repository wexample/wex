import click

from src.decorator.as_sudo import as_sudo


@click.command()
@click.pass_obj
@as_sudo
def core__core__install(kernel):
    pass

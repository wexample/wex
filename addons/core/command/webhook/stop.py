import click

from addons.core.command.webhook.serve import core__webhook__serve
from src.helper.system import kill_process_by_command
from src.helper.command import build_command_from_function
from src.decorator.as_sudo import as_sudo


@click.command()
@click.pass_obj
@as_sudo
def core__webhook__stop(
        kernel,
):
    kill_process_by_command(
        kernel,
        build_command_from_function(
            core__webhook__serve
        )
    )

    kernel.message(f'Webhook server stopped')

import click
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from src.core.Kernel import Kernel


def build_progress_bar(steps, **kwargs):
    return click.progressbar(
        steps,
        fill_char='▪',
        empty_char='⬝',
        color='cyan',
        **kwargs
    )


def progress_steps(kernel: Kernel, steps: [], title: str = 'Processing'):
    with build_progress_bar(steps, label=title) as progress_bar:
        for step in progress_bar:
            kernel.log(f'{title} : {step.__name__}')
            kernel.log_indent_up()

            response = step()

            kernel.log_indent_down()
            click.echo("\n")

            # Step failed somewhere
            if response is False:
                return


def prompt_choice(question, choices, default):
    envs = choices.copy()
    envs.append(
        Choice(value=None, name='> Abort')
    )

    return inquirer.select(
        message=question,
        choices=envs,
        default=default,
    ).execute()

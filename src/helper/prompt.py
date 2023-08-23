import click
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

def build_progress_bar(steps, **kwargs):
    return click.progressbar(
        steps,
        fill_char='▪',
        empty_char='⬝',
        color='cyan',
        **kwargs
    )


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

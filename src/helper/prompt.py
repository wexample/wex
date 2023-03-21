import click


def build_progress_bar(steps, **kwargs):
    return click.progressbar(
        steps,
        fill_char='▪',
        empty_char='⬝',
        color='cyan',
        **kwargs
    )

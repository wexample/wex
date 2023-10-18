import click


def app_dir_option(*args, **kwargs):
    def decorator(function):
        if callable(function):
            # Add the --app-dir option
            function = click.option(
                '--app-dir',
                '-a',
                type=str,
                help="App directory",
                **kwargs
            )(function)
        return function

    return decorator

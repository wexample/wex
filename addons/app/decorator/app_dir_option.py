import click


def app_dir_option(*args, **kwargs):
    def decorator(f):
        if callable(f):
            # Add the --app-dir option
            f = click.option('--app-dir', '-a', type=str, required=True, is_flag=True,
                             help="App directory")(f)

        return f

    return decorator

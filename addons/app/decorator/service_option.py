import click


def service_option():
    def decorator(f):
        if callable(f):
            # Add the --app-dir option
            f = click.option(
                "--service", "-s", type=str, required=True, help="Service name"
            )(f)

        return f

    return decorator

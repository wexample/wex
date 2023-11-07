import click


def option_webhook_url(*args, **kwargs):
    def decorator(function):
        if callable(function):
            function.option_webhook_url = True

            # Add the --app-dir option
            function = click.option(
                '--url',
                '-u',
                type=str,
                help="Webhook url",
                **kwargs
            )(function)
        return function

    return decorator

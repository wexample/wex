import click


def option_webhook_listener(port=False, path=False):
    def decorator(function):
        if callable(function):
            if port:
                function.option_webhook_listener_port = True

                function = click.option(
                    '--port',
                    '-p',
                    type=int,
                    help="Webhook listener port number",
                )(function)

            if path:
                function.option_webhook_listener_path = True

                function = click.option(
                    '--path',
                    '-p',
                    type=str,
                    help="Webhook requested path",
                )(function)

        return function

    return decorator

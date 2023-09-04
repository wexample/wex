import click


def response_collection(*args, **kwargs):
    def decorator(f):
        if callable(f):
            # Add a default option
            f = click.option(
                '--response-collection-step',
                type=int,
                default=None,
                help='Step position, first call will be None, then other calls will increment'
            )(f)

            f.response_collection = True
        return f

    return decorator

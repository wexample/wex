import click


# Define your custom decorator
def option(*args, **kwargs):
    def decorator(f):
        if callable(f):
            # Apply the original click.option decorator
            f = click.option(*args, **kwargs)(f)
        return f

    return decorator

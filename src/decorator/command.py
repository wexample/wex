import click


# Define your custom decorator
def command(*args, **kwargs):
    if 'help' not in kwargs:
        raise ValueError("The 'help' argument is required for the custom command decorator.")

    def decorator(f):
        if callable(f):
            # Apply the click.pass_obj decorator
            f = click.pass_obj(f)
            # Apply the original click.command decorator
            f = click.command(*args, **kwargs)(f)
        return f

    return decorator

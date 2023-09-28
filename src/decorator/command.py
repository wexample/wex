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

            # Add verbosity levels
            f = click.option('--quiet', '-quiet', is_flag=True, required=False, help="Silent all logs")(f)
            f = click.option('--vv', '-vv', is_flag=True, required=False, help="More verbosity")(f)
            f = click.option('--vvv', '-vvv', is_flag=True, required=False, help="Maximum verbosity")(f)

            # Step position control
            f = click.option('--command-request-step', '-command-request-step', type=str, required=False,
                             help="Core option for processes collection execution")(f)
            f = click.option('--kernel-task-id', '-kernel-task-id', type=str, required=False,
                             help="Core option for processes collection execution")(f)
            f = click.option('--log-indent', '-log-indent', type=str, required=False,
                             help="Core option for processes collection execution")(f)
        return f

    return decorator

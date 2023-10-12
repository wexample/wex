import click

COMMAND_HELP_PARAMS = [
    'fast_mode',
    'quiet',
    'vv',
    'vvv',
    'command_request_step',
    'kernel_task_id',
    'log_indent',
    'log_length'
]


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
            f = click.option('--fast-mode', '-fast-mode', is_flag=True, required=False,
                             help="Disable queued scripts execution. Will be faster, but less interactive.")(f)
            f = click.option('--quiet', '-quiet', is_flag=True, required=False,
                             help="Silent all logs")(f)
            f = click.option('--vv', '-vv', is_flag=True, required=False,
                             help="More verbosity")(f)
            f = click.option('--vvv', '-vvv', is_flag=True, required=False,
                             help="Maximum verbosity")(f)

            # Step position control
            f = click.option('--command-request-step', '-command-request-step', type=str, required=False,
                             help="Core option for processes collection execution")(f)
            f = click.option('--kernel-task-id', '-kernel-task-id', type=str, required=False,
                             help="Core option for processes collection execution")(f)
            f = click.option('--log-indent', '-log-indent', type=str, required=False,
                             help="Core option for processes collection execution")(f)
            f = click.option('--log-length', '-log-length', type=int, required=False,
                             help="Change logging frame height, set 0 to disable it")(f)
        return f

    return decorator

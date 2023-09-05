from src.decorator.command import command


def test_command(*args, **kwargs):
    if 'help' not in kwargs:
        kwargs['help'] = 'A test command'

    def decorator(f):
        f = command(*args, **kwargs)(f)

        f.test_command = True

        return f

    return decorator

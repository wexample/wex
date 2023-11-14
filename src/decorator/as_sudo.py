from src.core.FunctionProperty import FunctionProperty


def as_sudo():
    def decorator(function):
        # Say that the function is not allowed to be executed without sudo permissions.
        FunctionProperty(
            function,
            'as_sudo',
            True)

        return function

    return decorator

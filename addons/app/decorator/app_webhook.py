from src.core.FunctionProperty import FunctionProperty


def app_webhook(*args, **kwargs):
    def decorator(function):
        FunctionProperty(
            function,
            'app_webhook',
            True)

        return function

    return decorator

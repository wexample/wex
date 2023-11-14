from src.core.FunctionProperty import FunctionProperty


def app_webhook(name: str, *args, **kwargs):
    def decorator(function):
        FunctionProperty(
            function,
            'app_webhook',
            name)

        return function

    return decorator

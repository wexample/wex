

def app_webhook(*args, **kwargs):
    def decorator(function):
        function.is_app_webhook = True

        return function

    return decorator

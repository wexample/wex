def no_log():
    def decorator(function):
        # Say that the function execution is not stored in log file,
        # Used for log command itself or autocomplete suggestion.
        function.no_log = True
        return function

    return decorator

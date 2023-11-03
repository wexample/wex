def verbosity(level: int):
    def decorator(function):
        # Enforce verbosity level for this function.
        function.verbosity = level
        return function

    return decorator

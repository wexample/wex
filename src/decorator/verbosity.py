from src.core.FunctionProperty import FunctionProperty


def verbosity(level: int):
    def decorator(function):
        # Enforce verbosity level for this function.
        FunctionProperty(function, "verbosity", level)

        return function

    return decorator

def alias(name: bool | str = True):
    def decorator(func):
        if hasattr(func, 'aliases'):
            func.aliases.append(name)
        else:
            func.aliases = [name]
        return func

    return decorator

from src.core.FunctionProperty import FunctionProperty


def alias(name: bool | str = True):
    def decorator(func):
        aliases = FunctionProperty.get_property(func, 'aliases')
        if aliases:
            aliases.append(name)
        else:
            FunctionProperty(
                func,
                'aliases',
                [name])

        return func

    return decorator

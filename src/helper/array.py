def array_unique(array):
    return list(
        set(array)
    )


def array_replace_value(array: list, search, replacement) -> list:
    return [replacement if value == search else value for value in array]

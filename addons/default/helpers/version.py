def is_greater_than(first, second, true_if_equal=False):
    keys_to_check = [
        'major',
        'intermediate',
        'minor',
        'pre_build_type',
        'pre_build_number'
    ]

    for key in keys_to_check:
        first_value = first.get(key, None)
        second_value = second.get(key, None)

        if first_value is None and second_value is not None:
            return False
        elif first_value is not None and second_value is None:
            return True

        if first_value is not None and second_value is not None:
            if first_value < second_value:
                return False
            elif first_value > second_value:
                return True

    return true_if_equal


def version_join(version: dict, add_build: bool = False) -> str:
    output = f"{version['major']}.{version['intermediate']}.{version['minor']}"

    # Build version string
    version['pre_build_info'] = ''
    if version['pre_build_type']:
        output += f'-{version["pre_build_type"]}.{version["pre_build_number"]}'

    if add_build:
        import datetime
        output += f'+build.' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    return output

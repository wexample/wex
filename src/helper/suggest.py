from src.helper.registry import get_all_commands
from src.const.globals import COMMAND_SEPARATOR_GROUP


def suggest_autocomplete_if_single(kernel, search_string):
    all_commands = get_all_commands(kernel)

    all_commands = [
        name for name in all_commands if name.startswith(search_string)
    ]

    if len(all_commands) == 1:
        # Adding a trailing space indicates
        # that command is found
        return all_commands[0] + ' '

    return search_string


def suggest_from_path(commands_path: str, search_string: str, prefix: str) -> []:
    from src.helper.registry import scan_commands_groups

    commands = scan_commands_groups(commands_path, prefix)
    commands_names = []

    for command, command_data in commands.items():
        commands_names.append(command)

    # Ignore non relevant values
    commands_names = [
        name for name in commands_names if name.startswith(search_string)
    ]

    return commands_names


def get_all_services_names_suggestions(kernel):
    from src.helper.registry import get_all_services_names

    return ' '.join([
        f'@{service}' for service in get_all_services_names(kernel)]
    )

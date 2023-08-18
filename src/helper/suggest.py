from src.const.globals import COMMAND_SEPARATOR_GROUP


def suggest_from_path(path: str, search_string: str) -> str:
    import os
    from src.helper.registry import scan_commands_groups
    from addons.app.const.app import APP_DIR_APP_DATA

    commands = scan_commands_groups(path + APP_DIR_APP_DATA + 'command/', '.')
    commands_names = []

    # User typed "wex .group/" and expect command name
    if COMMAND_SEPARATOR_GROUP in search_string:
        for command, command_data in commands.items():
            commands_names.append(command)

        # Ignore non relevant values
        commands_names = [
            name for name in commands_names if name.startswith(search_string)
        ]

        suggestion = ' '.join(commands_names)
    else:
        groups = []
        for command, command_data in commands.items():
            groups.append(command.split('/')[0])
            commands_names.append(command)

        # Ignore non relevant values
        groups = [
            name for name in groups if name.startswith(search_string)
        ]

        suggestion = ' '.join(groups)

        # There is only one group matching search
        if len(groups) == 1:
            full_commands = [
                name for name in commands_names if name.startswith(search_string)
            ]

            # There is only one command in this group
            if len(full_commands) == 1:
                # Override suggestion with full command
                suggestion = full_commands[0]
            else:
                # Prepare user to search command name part
                suggestion += COMMAND_SEPARATOR_GROUP

    return suggestion


def get_all_services_names_suggestions(kernel):
    from src.helper.registry import get_all_services_names

    return ' '.join([
        f'@{service}' for service in get_all_services_names(kernel)]
    )

import click

from src.const.globals import COMMAND_SEPARATOR_ADDON, COMMAND_SEPARATOR_GROUP, COMMAND_CHAR_APP, COMMAND_CHAR_SERVICE, \
    COMMAND_CHAR_USER


@click.command
@click.pass_obj
@click.option('--cursor', '-c', type=int, required=True, help="Indicates which part of search string is focused")
@click.option('--search', '-s', type=str, required=True, help="Separated arguments, without first command, i.e. : "
                                                              "app :: config/write")
def core__autocomplete__suggest(kernel, cursor: int, search: str) -> str:
    """
    Works and interact with cli/autocomplete bash command to provide a smart autocomplete integration.
    Returns a string with suggestions to transmit to bash compgen.
    """
    suggestion = ''

    search_split = search.split(' ')

    # Mismatch between parts and cursor index.
    if cursor > len(search_split):
        return ''

    search_part = search_split[cursor]

    if cursor == 0:
        # User typed "wex ~"
        if search_split[0] == COMMAND_CHAR_USER:
            import os
            from src.helper.suggest import suggest_from_path
            from addons.app.const.app import APP_DIR_APP_DATA

            suggestion = suggest_from_path(
                f'{os.path.expanduser("~")}/',
                search_split[0]
            )
        # User typed "wex ."
        elif search_split[0].startswith(COMMAND_CHAR_APP):
            from addons.app.command.location.find import app__location__find
            from src.helper.suggest import suggest_from_path

            app_path = kernel.exec_function(app__location__find)
            # We are in an app dir or subdir
            if app_path:
                suggestion = suggest_from_path(app_path, search_split[0])

        # User typed "wex @"
        elif search_split[0] == COMMAND_CHAR_SERVICE:
            from src.helper.suggest import get_all_services_names_suggestions

            suggestion = get_all_services_names_suggestions(kernel)
        # User typed "wex ", we suggest all addons names and special chars.
        else:
            suggestion = ' '.join(addon + '::' for addon in kernel.registry['addons'].keys())
            # Adds also all core actions.
            suggestion += ' ' + ' '.join(kernel.get_core_actions().keys())
            # Suggest to execute service command
            suggestion += f' \\{COMMAND_CHAR_SERVICE}'

            import os
            from addons.app.const.app import APP_DIR_APP_DATA
            # User local command path exists
            base_path = f'{os.path.expanduser("~")}/{APP_DIR_APP_DATA}command'
            if os.path.exists(base_path):
                # Suggest to execute local user command
                suggestion += f' \\{COMMAND_CHAR_USER}'

            from addons.app.command.location.find import app__location__find
            # We are in an app dir or subdir
            if kernel.exec_function(app__location__find):
                # Suggest to execute local app command
                suggestion += f' \\{COMMAND_CHAR_APP}'

    elif cursor == 1:
        # User typed "wex @x" so we can suggest service names.
        if search_split[0] == COMMAND_CHAR_SERVICE:
            if COMMAND_SEPARATOR_GROUP in search_split[1]:
                split = search_split[1].split('/', 1)
                service_name = split[0]

                if service_name in kernel.registry['services']:
                    from src.helper.registry import get_all_commands
                    commands = get_all_commands({service_name: kernel.registry['services'][service_name]})

                    return ' '.join(commands)
            else:
                from src.helper.suggest import get_all_services_names_suggestions

                suggestion = get_all_services_names_suggestions(kernel)
                # If there's only one suggestion (no space separator), add a trailing "/" at the end
                if ' ' not in suggestion:
                    suggestion += COMMAND_SEPARATOR_GROUP
        # User typed "app::", we suggest all addon groups.
        elif search_split[1] == COMMAND_SEPARATOR_ADDON:
            from src.helper.registry import get_commands_groups_names
            suggestion = ' '.join(get_commands_groups_names(kernel, search_split[0]))
        else:
            # User types "app:", we add a second ":"
            suggestion = ':'
    elif cursor == 2:
        addon = search_split[0]

        if addon in kernel.registry['addons']:
            # User typed "wex app::conf", we suggest full addon commands list.
            for command, command_data in kernel.registry['addons'][addon]['commands'].items():
                command_parts = command.split(COMMAND_SEPARATOR_ADDON)
                command_split = command_parts[1].split(COMMAND_SEPARATOR_GROUP)

                if COMMAND_SEPARATOR_GROUP in search_part:
                    if command_split[0] == search_split[2].split(COMMAND_SEPARATOR_GROUP)[0]:
                        suggestion += f' {" ".join(command_parts)}'
                else:
                    suggestion += f' {command_split[0]}'

            # Reduce unique values
            suggestion = " ".join(set(suggestion.split()))
    # Complete arguments.
    elif cursor >= 3:
        processor = kernel.build_command_processor(
            ''.join(search_split[0:3])
        )

        if not processor:
            return ''

        params_current = [val for val in search_split[3:] if val.startswith("-")]

        # Merge all params in a list,
        # but ignore already given args,
        # i.e : if -d is already given, do not suggest "-d" or "--default"
        function = processor.get_function(kernel)
        params = []
        for param in function.params:
            if any(opt in params_current for opt in param.opts):
                continue
            params += param.opts

        suggestion = ' '.join(params)

    return suggestion

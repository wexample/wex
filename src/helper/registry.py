def get_commands_groups_names(kernel, addon):
    group_names = set()

    if addon in kernel.registry['addons']:
        for command in kernel.registry['addons'][addon]['commands'].keys():
            group_name = command.split("::")[1].split("/")[0]
            group_names.add(group_name)
    return list(group_names)


def get_all_commands(kernel):
    output = {}

    for addon, addon_data in kernel.registry['addons'].items():
        for command, command_data in addon_data['commands'].items():
            output[command] = command_data

    return output

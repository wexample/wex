from src.helper.registry import find_commands_by_function_property


def find_command_by_webhook(kernel, name: str):
    commands = find_commands_by_function_property(
        kernel,
        'app_webhook'
    )

    for command in commands:
        if ('app_webhook' in commands[command]['properties']
                and commands[command]['properties']['app_webhook'] == name):
            return commands[command]

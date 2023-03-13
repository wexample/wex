def command_to_path(command: str) -> str:
    """
    Convert addon::group/name to addon/command/group/name.py

    :param command: full command
    :return: file path
    """
    return command.replace("::", "/").replace("/", "/command/") + ".py"

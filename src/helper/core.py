def core_get_version(path: str) -> str:
    with open(f'{path}version.txt', 'r') as file:
        return file.read().strip()

from src.const.globals import FILE_VERSION


def core_get_version(path: str) -> str:
    with open(f'{path}{FILE_VERSION}', 'r') as file:
        return file.read().strip()

def core_get_version(kernel) -> str:
    with open(f'{kernel.path["root"]}version.txt', 'r') as file:
        return file.read().strip()

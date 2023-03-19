import ast
import click

from src.const.globals import PATH_GLOBALS


@click.command
@click.pass_obj
@click.option('--key', '-k', type=str, required=True)
@click.option('--value', '-v', type=str, required=True)
@click.option('--verbose', '-vv', type=bool, required=False, default=False)
def core_globals_set(kernel, key: str, value, verbose=False):
    file = kernel.path['root'] + PATH_GLOBALS

    if verbose:
        kernel.log(f'Set global {key} = {value} in {file}')

    with open(file, 'r') as f:
        source = f.read()
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and node.targets[0].id == key:
            node.value.s = value

    with open(file, 'w') as f:
        f.write(ast.unparse(tree))

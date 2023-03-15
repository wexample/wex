import ast
import click


@click.command
@click.pass_obj
@click.option('--key', '-k', type=str, required=True)
@click.option('--value', '-v', type=str, required=True)
def core_globals_set(kernel, key, value):
    file = kernel.path['root'] + 'src/const/globals.py'

    with open(file, 'r') as f:
        source = f.read()
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and node.targets[0].id == key:
            node.value.s = value

    with open(file, 'w') as f:
        f.write(ast.unparse(tree))

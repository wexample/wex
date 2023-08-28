import click


@click.command()
@click.option('--option', '-o', is_flag=True, required=False,
              help="A first option as flag")
@click.option('--another-option', '-ao', is_flag=True, required=False,
              help="Another option")
def test_2__another_demo_command__test(option=None, another_option=None):
    return 'FIRST'

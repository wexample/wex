import click


@click.command()
@click.option('--option', '-o', is_flag=True, required=False,
              help="A first option as flag")
@click.option('--another-option-third', '-aot', is_flag=True, required=False,
              help="Another option")
def test__demo_command_2__third(option=None, another_option_third=None):
    return 'THIRD'

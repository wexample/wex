import click

import socket


@click.command()
def system__system__ip() -> str:
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return ip_address

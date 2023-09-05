import socket

from src.core.Kernel import Kernel
from src.decorator.command import command


@command(help="Return the current system local IP")
def system__system__ip(kernel: Kernel) -> str:
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return ip_address

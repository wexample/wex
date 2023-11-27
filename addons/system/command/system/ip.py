import socket
from typing import TYPE_CHECKING

from src.decorator.command import command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Return the current system local IP")
def system__system__ip(kernel: 'Kernel') -> str:
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return ip_address

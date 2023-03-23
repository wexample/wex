import psutil
from typing import Optional
import os
import grp


def get_processes_by_port(port: int) -> Optional[psutil.Process]:
    for process in psutil.process_iter():
        try:
            connections = process.connections()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
        for connection in connections:
            if connection.laddr.port == port:
                return process
    return None


def get_sudo_group():
    return grp.getgrgid(os.getgid()).gr_name or os.environ.get('SUDO_GID')

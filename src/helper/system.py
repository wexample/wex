import psutil
from typing import Optional


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

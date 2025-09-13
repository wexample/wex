from __future__ import annotations

from typing import List

from src.core.command.resolver.AbstractCommandResolver import AbstractCommandResolver
from src.core.command.resolver.AddonCommandResolver import AddonCommandResolver
from src.core.command.resolver.AppCommandResolver import AppCommandResolver
from src.core.command.resolver.ServiceCommandResolver import ServiceCommandResolver
from src.core.command.resolver.UserCommandResolver import UserCommandResolver

COMMAND_RESOLVERS_CLASSES: list[type[AbstractCommandResolver]] = [
    AddonCommandResolver,
    ServiceCommandResolver,
    AppCommandResolver,
    UserCommandResolver,
]
